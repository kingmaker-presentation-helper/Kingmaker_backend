# import os
# from pdf2image import convert_from_bytes
# import comtypes.client

# ppt_name = "presentation.ppt"

# # 서버에 ppt 저장
# def save_ppt(ppt_bytes, path):
#     ppt = os.path.join(path, ppt_name)
#     with open(ppt, "wb") as ppt_file:
#         ppt_file.write(ppt_bytes)
#     print("save_ppt: success: ", ppt)


# # ppt를 pdf로 변환해서 서버에 저장, pdf 주소 반환
# def ppt2pdf(path):
#     ppt = os.path.join(path, ppt_name)

#     print('ppt2pdf: ', ppt)
#     print('현재 위치:', os.getcwd())

#     powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
#     powerpoint.Visible = True
#     slides = powerpoint.Presentations.Open(ppt)

#     file_name = os.path.splitext(ppt_name)[0]
#     output = os.path.join(path, file_name + ".pdf")

#     slides.SaveAs(output, FileFormat=32)
#     slides.Close()

#     powerpoint.Quit()
#     print("ppt2pdf: success")
#     return output


# # pdf 슬라이드를 이미지로 변환 및 저장, 이미지 목록 반환
# def pdf2img(pdf, path):
#     images = convert_from_bytes(open(pdf, "rb").read(), fmt="png")
    
#     image_paths = []

#     for i, image in enumerate(images):
#         image_path = f"{path}/slide_{i+1}.png"
#         image.save(image_path)
#         image_paths.append(image_paths)
#     print("pdf2img: success")
#     return image_paths