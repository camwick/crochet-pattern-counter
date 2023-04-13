from PIL import Image, ImageFont, ImageDraw

class PixelCounter:
    def __init__(self, imgPath, width, length) -> None:
        self.img = Image.open(imgPath)
        self.img = self.img.convert("RGB")
        self.borderColor = self.img.getpixel((0, 0))
        self.width = width
        self.length = length
        self.trueWidth, self.trueLength = self.img.size
        self.counts = []
    
        self.approximateSqrSize = (self.trueWidth // self.width, self.trueLength // self.length)

    def count(self):
        img_editable = ImageDraw.Draw(self.img)
        
        for y in range(1 , self.trueLength, self.approximateSqrSize[1] + 1):
            rowCounts = []

            count = 0
            prevColor = self.img.getpixel((1, y))

            xCoord = 0

            for x in range(2, self.trueWidth, self.approximateSqrSize[0] + 1):
                currentColor = self.img.getpixel((x, y))
                
                if prevColor == currentColor:
                    count += 1
                else:
                    rowCounts.append((prevColor, count))
                    
                    if count > 4:
                        typeX = xCoord
                        typeY = y

                        # adjust x and y values for typing
                        countStr = str(count)
                        if prevColor == (0, 0, 0):
                            fontColor = (255, 255, 255)

                            while self.img.getpixel((typeX, typeY)) == self.borderColor:
                                typeX -= 1
                            typeX += 2
                            # while self.img.getpixel((typeX, typeY)) == self.borderColor:
                            #     typeY -= 1
                            # typeY += 1
                        else:
                            fontColor = (0, 0, 0)

                            while self.img.getpixel((typeX, typeY)) != self.borderColor:
                                typeX -= 1
                            typeX += 1
                            while self.img.getpixel((typeX, typeY)) != self.borderColor:
                                typeY -= 1
                            typeY += 1
                            
                        numShift = 0
                        for num in countStr:
                            self.writeNum(img_editable, (typeX + (numShift * self.approximateSqrSize[0]), typeY), num, fontColor)
                            numShift += 1
                
                    count = 1
                    prevColor = currentColor
                    xCoord = x


            if count > 4:
                typeX = xCoord
                typeY = y

                #write the count on the picture
                count = str(count)
                if prevColor == (0, 0, 0):
                    fontColor = (255, 255, 255)

                    while self.img.getpixel((typeX, typeY)) == self.borderColor:
                        typeX -= 1
                    typeX += 2
                    # while self.img.getpixel((typeX, typeY)) == self.borderColor:
                    #     typeY -= 1
                    # typeY += 1
                else:
                    fontColor = (0, 0, 0)

                    while self.img.getpixel((typeX, typeY)) != self.borderColor:
                        typeX -= 1
                    typeX += 1
                    while self.img.getpixel((typeX, typeY)) != self.borderColor:
                        typeY -= 1
                    typeY += 1
                
                numShift = 0
                for num in count:
                    self.writeNum(img_editable, (typeX + (numShift * self.approximateSqrSize[0]), typeY), num, fontColor)
                    numShift += 1

            rowCounts.append((prevColor, count))

            self.counts.append(rowCounts)

        
        self.img.save("result.png")

    def writeNum(self, img, coord, num, color):
        font = ImageFont.truetype("calibri", self.approximateSqrSize[0] + 3)

        img.text(coord, str(num), color, font=font)

def main():
    width = 36
    length = 45
    imgPath = "test.png"

    counter = PixelCounter(imgPath, width, length)    
    counter.count()
    # counter.writeCounts()


if __name__ == "__main__":
    main()