# encoding: utf-8
"""
puts a five color water mark at the bottom-right of an image
and asks for a message to store within the image
the script can be run in a directory and will process all files
with extension jpg or jpeg, adding an extension png
"""
import os
import cv2

rgb_colors = [(65,105,25),(255,0,0),(46,139,87),(135,206,250),(255,215,0)]

# loop and wait for pictures to come in the directory
while True:
  for f in os.listdir("."):
    if f.endswith("jpeg") | f.endswith("jpg"):
      print("processing: ",f)
      cap = cv2.VideoCapture(f)
      ret, frame = cap.read()
      if ret:
        # defining the length of the short side of image
        height=frame.shape[0]
        width=frame.shape[1]
        # frame is of type numpy.ndarray
        # each bit can be set directly with
        # frame[l][c]=   where l = 0 to height-1 and c = 0 to width -1
        signature=frame.flat[((height-2)*width*3)-240:((height-2)*width*3)]
        valid_signature=[0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 0, 215, 255, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 250, 206, 135, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 87, 139, 46, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65, 25, 105, 65]
        if list(signature) == valid_signature:
          print("(info) image is watermarked")
          signature1=frame.flat[((height)*width*3)-240:((height)*width*3)]

          if list(signature1) != valid_signature:

            i=len(signature1.flat)

            ll=''
            while signature1.flat[i-1] in [48,49,50,51,52,53,54,55,56,57]:
              ll=ll+chr(int(signature1.flat[i-1]))
              i=i-1
            print("(info) it contains a message of length:" ,ll,":")
            pix_available=(height-1)*width
            message_len=int(ll)
            skip=int(pix_available/message_len)
            i=0
            message=''.encode("UTF-8")
            while i < message_len:
              message=message+int(frame.flat[i*skip*3]).to_bytes(1,'big')
              i=i+1
            print(message.decode("UTF-8"))
        i=0
        for g in rgb_colors:
          cv2.rectangle(frame,(((width-1)-(i*16)),(height-1)),(((width)-(i+1)*16),height-16),(g[2],g[1],g[0]),-1)
          i=i+1
        # now let's use the blue channel to insert a message in the picture
        # we start a 0,0 and distribute letters equally over the height-1 x width pixels
        # the bottom line of pixels is used for "meta data", i.e. the length of the message.
        message = str(input("what is the new message?")).encode("UTF-8")
        message_len = len(message)
        message_len1 = str(message_len).encode("ASCII")
        pix_available=(height-1)*width
        if message_len != 0:
          skip=int(pix_available/message_len)
          i=0
          for x in message:
            frame.flat[i*skip*3]=int(x)
            i=i+1
          i=1
          for x in message_len1:

            frame.flat[len(frame.flat)-i]=int(x)
            i=i+1
          frame.flat[len(frame.flat)-i]=100
        cv2.imwrite(f+'.png',frame)
        os.remove(f)
      else:
        print("Could not read picture")
      cap.release()
