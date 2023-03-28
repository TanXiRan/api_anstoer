from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from typing import List
from conf import *
import os
import random
from datetime import datetime
import time

router = APIRouter(prefix="/file", tags=["file"])


def gen_random_path(filename: str):
    img_type = '.' + filename.split('.')[-1]
    alps = 'abcdefghijklmnopqrstuvwxyz0123456789'
    timestr = int(time.time())
    random_chars = ''.join(random.sample(alps, 4))
    path = str(timestr) + random_chars + img_type
    return path


@router.get("/posters/{poster_name}")
async def read_poster(poster_name: str):
    return FileResponse(f"./media/posters/{poster_name}")


@router.post("/{posters}")
async def upload_poster(files: List[UploadFile] = File(...)):
    try:
        path_ls = []
        for file in files:
            filename = file.filename
            random_path = gen_random_path(filename=filename)
            save_path = os.path.join(POSTER_PATH, random_path)
            if not os.path.exists(save_path):
                with open(save_path, "wb") as f:
                    data = await file.read()
                    f.write(data)
            # path_ls.append({filename: os.path.join(REQUEST_POSTER_PATH, filename)})
            # path_ls.append(filename)
            path_ls.append(random_path)
        return {"status": "success", "poster_pathes": path_ls}
    except Exception as e:
        print(e)
        return {"status": "fail"}
