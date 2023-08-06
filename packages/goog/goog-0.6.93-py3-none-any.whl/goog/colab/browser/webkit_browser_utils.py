from playwright.sync_api import Browser, BrowserContext, Page, Download
driver = Browser(...)
context = BrowserContext(...)
page = Page(...)
from html2text import html2text
delay = 50
wait_delay = 50
type_delay = 0
try:
    from typing import Literal
except:
    from typing_extensions import Literal


def test():
    return page.evaluate('''()=>{
    return !0;
}
''')


def click_connect_button():
    return page.evaluate('''()=>{
    let e=document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector("#connect");
    return !!(e&&e.click()||true);
}
''')


def get_runtime_type():
    page.click("#runtime-menu-button", delay=delay)
    page.click("[command='change-runtime-type']", delay=delay)
    r = page.query_selector("#accelerator").input_value()
    page.click("#notebook-settings #cancel", delay=delay)
    return r or None


def set_runtime_type(type: Literal[None, "GPU", "TPU"]):
    page.click("#runtime-menu-button", delay=delay)
    page.click("[command='change-runtime-type']", delay=delay)
    page.select_option("#accelerator", "" if type is None else type)
    page.click("#notebook-settings #ok", delay=delay)
    return True


def is_connected():
    page.click("#runtime-menu-button", delay=delay)
    r = page.evaluate('''()=>!document.querySelector(".goog-menuitem-disabled[command='restart']");''')
    page.click("#runtime-menu-button", delay=delay)
    return r


def disconnect_runtime():
    if not is_connected():
        return True
    page.click("#runtime-menu-button", delay=delay)
    page.click("[command='powerwash-current-vm']", delay=delay)
    page.click(".yes-no-dialog #ok", delay=delay)
    return True


def connect_runtime():
    if is_connected():
        return True
    return click_connect_button()


def reset_pointer():
    page.query_selector("#top-toolbar").click(delay=delay)


def restart_runtime():
    reset_pointer()
    page.keyboard.down("Control")
    page.wait_for_timeout(wait_delay)
    page.keyboard.press("m", delay=delay)
    page.wait_for_timeout(wait_delay)
    page.keyboard.up("Control")
    page.wait_for_timeout(wait_delay)
    page.keyboard.press("Period", delay=delay)
    page.wait_for_timeout(wait_delay)
    page.click(".yes-no-dialog #ok", delay=delay)
    return True


def get_cells_length():
    return len(page.query_selector_all("div.cell.code"))


def get_all_cells_code():
    r = [[
        _.scroll_into_view_if_needed(),
        "\n".join(__.inner_text() for __ in _.query_selector_all(".main-content .view-line"))
    ][1] for _ in page.query_selector_all("div.cell.code")]
    return [_.replace("\xa0", " ") for _ in r]


def get_cell_code(i):
    r = page.query_selector_all("div.cell.code")[i]
    r.scroll_into_view_if_needed()
    r = "\n".join(__.inner_text() for __ in r.query_selector_all(".main-content .view-line"))
    return r.replace("\xa0", " ")


def get_all_cells_output():
    r = []
    for _ in page.query_selector_all("div.cell.code"):
        _.scroll_into_view_if_needed()
        __ = _.query_selector(".main-content .output iframe")
        if __:
            r.append(html2text(__.content_frame().content()))
        else:
            __ = _.query_selector(".main-content .output .output-content")
            r.append(html2text(__.inner_html()))
    return [_.replace("\xa0", " ") for _ in r]


def get_cell_output(i):
    r = page.query_selector_all("div.cell.code")[i]
    r.scroll_into_view_if_needed()
    __ = r.query_selector(".main-content iframe")
    if __:
        __ = __.content_frame()
        r = html2text(__.content())
    else:
        __ = r.query_selector(".main-content .output .output-content")
        r = html2text(__.inner_html())
    return r.replace("\xa0", " ")


def insert_cell():
    page.keyboard.down("Control")
    page.wait_for_timeout(wait_delay)
    page.keyboard.press("m", delay=delay)
    page.wait_for_timeout(wait_delay)
    page.keyboard.up("Control")
    page.keyboard.press("b", delay=delay)
    return True


def insert_cell_after(i):
    r = page.query_selector_all("div.cell.code")[i]
    r.scroll_into_view_if_needed()
    r.click(delay=delay)
    return insert_cell()


def insert_cell_before(i):
    r = page.query_selector_all("div.cell.code")[i-1]
    r.scroll_into_view_if_needed()
    r.click(delay=delay)
    return insert_cell()


def type_code(code):
    codes = code.splitlines()
    for code in codes:
        page.keyboard.type(code, delay=type_delay)
        page.keyboard.press("Enter", delay=type_delay)
        page.wait_for_timeout(wait_delay)
        page.keyboard.down("Shift")
        page.wait_for_timeout(wait_delay)
        page.keyboard.press("Home", delay=type_delay)
        page.wait_for_timeout(wait_delay)
        page.keyboard.up("Shift")
        page.wait_for_timeout(wait_delay)
        page.keyboard.press("Delete", delay=type_delay)
        page.wait_for_timeout(wait_delay)
    return True


def set_cell_code(i, code):
    insert_cell_after(i)
    r = page.query_selector_all("div.cell.code")[i+1]
    r.scroll_into_view_if_needed()
    r.click()
    type_code(code)
    delete_cell(i)
    return True


def delete_all_cells():
    reset_pointer()
    page.keyboard.down("Control")
    page.wait_for_timeout(wait_delay)
    page.keyboard.down("Shift")
    page.wait_for_timeout(wait_delay)
    page.keyboard.press("a", delay=delay)
    page.keyboard.up("Shift")
    page.wait_for_timeout(wait_delay)
    page.keyboard.up("Control")
    page.wait_for_timeout(wait_delay)
    page.keyboard.down("Control")
    page.wait_for_timeout(wait_delay)
    page.keyboard.down("m")
    page.wait_for_timeout(wait_delay)
    page.keyboard.press("d", delay=delay)
    page.wait_for_timeout(wait_delay)
    page.keyboard.up("m")
    page.wait_for_timeout(wait_delay)
    page.keyboard.up("Control")
    return True


def delete_cell(i):
    r = page.query_selector_all("div.cell.code")[i]
    r.scroll_into_view_if_needed()
    r.click(delay=delay)
    page.keyboard.down("Control")
    page.wait_for_timeout(wait_delay)
    page.keyboard.press("m", delay=delay)
    page.wait_for_timeout(wait_delay)
    page.keyboard.up("Control")
    page.wait_for_timeout(wait_delay)
    page.keyboard.press("d", delay=delay)
    return True


def run_cell(i):
    r = page.query_selector_all("div.cell.code")[i]
    r.scroll_into_view_if_needed()
    r.click(delay=delay)
    page.keyboard.down("Control")
    page.wait_for_timeout(wait_delay)
    page.keyboard.press("Enter", delay=delay)
    page.wait_for_timeout(wait_delay)
    page.keyboard.up("Control")
    return True


def screenshot():
    return page.screenshot()


def upload_file(path):
    input = page.query_selector("input[type='file'][multiple]")
    if not input:
        page.query_selector("[command='show-files']").click(delay=delay)
    input = page.query_selector("input[type='file'][multiple]")
    print(input)
    input.set_input_files([path])
    input.dispatch_event("change")
    ok = page.query_selector(".buttons #ok")
    print(ok)
    if ok:
        ok.click(delay=delay)
    return True


def set_download_location(path, listeners=[]):
    def rm():
        if listeners:
            for _ in listeners:
                try:
                    page.remove_listener("download", _)
                except:
                    pass
            listeners.clear()
    rm()
    def download(dl: Download):
        import shutil
        import time
        import os
        try:
            fp = dl.path()
            if fp:
                fp = str(fp.absolute())
                dst = os.path.join(path, dl.suggested_filename)
                if os.path.isfile(dst):
                    dst += ".{}".format(time.time())
                shutil.move(fp, dst)
        except:
            pass
        rm()
    listeners.append(download)
    page.once("download", download)
    return True


def download_file(path, save_path):
    import json
    import time
    set_download_location(save_path)
    insert_cell_after(0)
    set_cell_code(1, '''from google.colab import files
files.download({})'''.format(json.dumps(path)))
    run_cell(1)
    delete_cell(1)
    return True




