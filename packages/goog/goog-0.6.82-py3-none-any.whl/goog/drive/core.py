from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import GoogleDriveFile
import os
from typing import List, Callable


def set_client_config_path(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    GoogleAuth.DEFAULT_SETTINGS["client_config_file"] = path


GoogleAuth.DEFAULT_SETTINGS["get_refresh_token"] = True


class GDrive:
    def __init__(
            self,
            session, # type: str
            auto_renew_session=True, # type: bool
    ):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(session)
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            if auto_renew_session:
                gauth.Refresh()
            else:
                raise Exception("session expired", session)
        else:
            gauth.Authorize()
        gauth.SaveCredentialsFile(session)
        self.gdrive = GoogleDrive(gauth)
        self.cache = {}
        self.parents = {}

    def _patch_GoogleDriveFile(self, r):
        if isinstance(r, list):
            return [self._patch_GoogleDriveFile(_) for _ in r]
        if not isinstance(r, GoogleDriveFile):
            raise TypeError(r, "is not pydrive2.files.GoogleDriveFile")
        is_file = r.metadata["mimeType"] != "application/vnd.google-apps.folder"
        r.is_file = is_file
        r.is_folder = not is_file
        return r

    def get_file_info(
            self,
            id, # type: str
    ) -> GoogleDriveFile:
        if id in self.cache:
            return self.cache[id]
        r = self.gdrive.CreateFile({"id": id})
        r.FetchMetadata()
        r = self._patch_GoogleDriveFile(r)
        r.metadata["path"] = None
        self.cache[id] = r
        return r

    def get_folder_info(
            self,
            id, # type: str
    ) -> GoogleDriveFile:
        if id in self.parents:
            return self.parents[id]
        r = self.gdrive.CreateFile({"id": id})
        r.FetchMetadata()
        r = self._patch_GoogleDriveFile(r)
        self.parents[id] = r
        return r

    def get_items_in_folder(
            self,
            id, # type: str
    ) -> List[GoogleDriveFile]:
        if id in self.cache:
            return self.cache[id]
        r = self.gdrive.ListFile({"q": "'{}' in parents".format(id)}).GetList()
        r = self._patch_GoogleDriveFile(r)
        for _ in r:
            if _.is_file:
                id2 = _.metadata["id"]
                if id2 not in self.cache:
                    self.cache[id2] = _
            parents = []
            pid = _.metadata["parents"][0]["id"]
            pparents = [pid]
            while pparents:
                pinfo = self.get_folder_info(pparents.pop(0))
                parents.append(pinfo["title"])
                pid = pinfo.metadata["parents"]
                if not pid:
                    continue
                pid = pid[0]["id"]
                pparents.append(pid)
            parents.reverse()
            path = "/".join([""]+parents)
            # if _.is_file:
            #     print(parents, path, _["id"])
            _.metadata["path"] = path
        self.cache[id] = r
        return r

    def get_all_items_in_folder(
            self,
            id, # type: str
            ignore_top_folder=False, # type: bool
    ) -> List[GoogleDriveFile]:
        items = []
        pending = [id]
        while pending:
            id = pending.pop(0)
            r = self.get_items_in_folder(id=id)
            for _ in r:
                if _.is_folder:
                    pending.append(_["id"])
                elif _.is_file:
                    items.append(_)
                    top_path = _.metadata["path"]
                    if ignore_top_folder:
                        top_path = top_path.split("/")
                        top_path.pop(1)
                        top_path = ("/"+"/".join(top_path)).replace("//", "/")
                    _.metadata["path"] = top_path
        return items

    def download_folder(
            self,
            id, # type: str
            save_path=None, # type: str
            ignore_top_folder=False, # type: bool
            cb=None, # type: Callable[[int, int, GoogleDriveFile], None]
            **kwargs
    ):
        items = self.get_all_items_in_folder(id=id)
        paths = []
        for ii, _ in enumerate(items):
            top_path = _.metadata["path"]
            if ignore_top_folder:
                top_path = top_path.split("/")
                top_path.pop(1)
                top_path = ("/"+"/".join(top_path)).replace("//", "/")
            fp = "/".join([top_path, _.metadata["title"]]).replace("//", "/")
            if save_path:
                fp = save_path+fp
            else:
                fp = fp[1:]
            if os.path.dirname(fp):
                os.makedirs(os.path.dirname(fp), exist_ok=True)
            args = dict(
                filename=fp,
                chunksize=10 * 1024 * 1024,
                acknowledge_abuse=True
            )
            args.update(kwargs)
            try:
                _.GetContentFile(**args)
            except Exception as e:
                if "acknowledge_abuse" in str(e):
                    args.pop("acknowledge_abuse")
                    _.GetContentFile(**args)
                else:
                    raise e
            paths.append(args["filename"])
            callable(cb) and cb(ii+1, len(items), _)
        return paths

    def download_file(
            self,
            id, # type: str
            save_path=None, # type: str
            **kwargs
    ):
        item = self.get_file_info(id=id)
        fp = item.metadata["title"]
        if save_path:
            fp = save_path+"/"+fp
        if os.path.dirname(fp):
            os.makedirs(os.path.dirname(fp), exist_ok=True)
        args = dict(
            filename=fp,
            chunksize=10 * 1024 * 1024,
            acknowledge_abuse=True
        )
        args.update(kwargs)
        try:
            item.GetContentFile(**args)
        except Exception as e:
            if "acknowledge_abuse" in str(e):
                args.pop("acknowledge_abuse")
                item.GetContentFile(**args)
            else:
                raise e
        return args["filename"]

