import subprocess as subp
from PIL import Image
from io import BytesIO

max_size = 4080
atomic_size = 16

def correct_size(img : Image):
    width, height = img.size
    width = (width // atomic_size) * atomic_size
    height = (height // atomic_size) * atomic_size
    if width > max_size:
        width = max_size
    if height > max_size:
        height = max_size
    return img.resize((width, height), resample=Image.BILINEAR)


def correct_palete(img : Image):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    return img


"""
Function working only with streams
"""
def encode(callsign : str, img_id : int, quality : int, img : Image):
    img = correct_size(img)
    img = correct_palete(img)
    with BytesIO() as bytes_io:
        img.save(bytes_io, format='JPEG')
        # bytes_io.seek(0)
        process = subp.Popen(
            args=["ssdv", "-e", "-c", callsign, "-i", str(img_id), "-q", str(quality)],
            stdin=subp.PIPE, stdout=subp.PIPE, bufsize=-1)
        (stdout, stderr) = process.communicate(input=bytes_io.getvalue())
        return BytesIO(stdout)
    pass

"""
Function working only with streams
"""
def decode(quality : int, bytes_io : BytesIO):
    process = subp.Popen(
        args=["ssdv", "-d", "-q", str(quality)],
        stdin=subp.PIPE, stdout=subp.PIPE, stderr=None)
    (stdout, stderr) = process.communicate(input=bytes_io.getvalue())
    bytes_io.close()
    return Image.open(BytesIO(stdout))


def main():
    print("SSDV streaming test application")
    
    callsign = "HA5KFU"
    img_id = 1
    quality = 5
    src_img_path = "./resources/input.png"
    binary_path = "./resources/encoded.bin"
    out_img_path = "./resources/output.jpeg"
    is_encode = True

    if is_encode:
        try:
            with Image.open(src_img_path, mode='r') as img, \
            encode(callsign, img_id, quality, img) as bytes_io, \
            open(binary_path, mode='wb') as out_file:
                out_file.write(bytes_io.getvalue())
            print("Encoding succeeded")
        except Exception as e:
            print("Encoding image has failed!", e)
    else:
        try:
            with open(binary_path, mode='rb') as in_binary, \
            BytesIO(in_binary.read()) as bytes_io, \
            decode(quality, bytes_io) as image:
                image.save(out_img_path)
            print("Decoding succeeded")
        except Exception as e:
            print("Decoding image has failed!", e)

if __name__ == "__main__":
    main()