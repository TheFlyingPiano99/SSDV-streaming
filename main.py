import subprocess as subp
from PIL import Image
from io import BytesIO, StringIO


def encode(callsign : str, img_id : int, quality : int, img : Image):    
    bytes_io = BytesIO()
    img.save(bytes_io, format='JPEG')
    bytes_io.seek(0)
    process = subp.Popen(
        args=["ssdv.exe", "-e", "-c", callsign, "-i", str(img_id), "-q", str(quality)],
        stdin=subp.PIPE, stdout=subp.PIPE, bufsize=-1)
    (stdout, stderr) = process.communicate(input=bytes_io.getvalue())
    return stdout


def decode(quality, binary):
    process = subp.Popen(
        args=["ssdv.exe", "-d", "-q", str(quality)],
        stdin=subp.PIPE, stdout=subp.PIPE, stderr=None)
    img = Image.open(process.stdout)
    return img


def main():
    print("SSDV streaming test application")
    
    callsign = "HA5KFU"
    img_id = 1
    quality = 5
    src_img_path = "./resources/image.jpeg"
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
            out_img = decode(in_binary)
            in_binary.close()
            out_img.save(out_img_path, format='JPEG')
        except Exception as e:
            print("Decoding image has failed!")
            print(e)

if __name__ == "__main__":
    main()