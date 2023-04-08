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
    bytes_io = BytesIO()
    img.save(bytes_io, format='JPEG')
    bytes_io.seek(0)
    process = subp.Popen(
        args=["ssdv.exe", "-e", "-c", callsign, "-i", str(img_id), "-q", str(quality)],
        stdin=subp.PIPE, stdout=subp.PIPE, bufsize=-1)
    (stdout, stderr) = process.communicate(input=bytes_io.getvalue())
    return stdout


"""
Function working only with streams
"""
def decode(quality, binary):
    process = subp.Popen(
        args=["ssdv.exe", "-d", "-q", str(quality)],
        stdin=subp.PIPE, stdout=subp.PIPE, stderr=None)
    (stdout, stderr) = process.communicate(input=binary)
    img = Image.open(stdout)
    return img


def main():
    print("SSDV streaming test application")
    
    callsign = "HA5KFU"
    img_id = 1
    quality = 5
    src_img_path = "./resources/input.jpeg"
    binary_path = "./resources/encoded.bin"
    out_img_path = "./resources/output.jpeg"
    is_encode = True

    if is_encode:
        try:
            img : Image = Image.open(src_img_path, mode='r')
            out_binary = encode(callsign, img_id, quality, img)
            out_file = open(binary_path, mode='wb')
            out_file.write(out_binary)
            out_file.close()
        except Exception as e:
            print("Encoding image has failed!")
            print(e)
    else:
        try:
            in_binary = open(binary_path, mode='rb')
            out_img = decode(quality, in_binary)
            in_binary.close()
            out_img.save(out_img_path, format='JPEG')
        except Exception as e:
            print("Decoding image has failed!")
            print(e)

if __name__ == "__main__":
    main()