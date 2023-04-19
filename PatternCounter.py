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
        self.approximateSqrSize = ((self.trueWidth - 1) // self.width , (self.trueLength - 1) // self.length)

        self.sampleColors()

    def count(self):
        img_editable = ImageDraw.Draw(self.img)
        
        for y in range(1 , self.trueLength, self.approximateSqrSize[1]):
            rowCounts = []

            count = 0
            prevColor = self.img.getpixel((1, y))

            xCoord = 1

            for x in range(1, self.trueWidth, self.approximateSqrSize[0]):
                currentColor = self.img.getpixel((x, y))

                if currentColor == self.borderColor:
                    temp1Color = self.img.getpixel((x, y-1))
                    temp2Color = self.img.getpixel((x, y+1))

                    temp3Color = self.img.getpixel((x-1, y))
                    temp4Color = self.img.getpixel((x+1, y))


                    if temp1Color != self.borderColor and temp2Color != self.borderColor:
                        currentColor = temp2Color
                        y += 1
                    if temp3Color != self.borderColor and temp4Color != self.borderColor:
                        currentColor = temp4Color
                        x += 1
                    
                
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

    def sampleColors(self):
        self.rows = set()
        self.columns = set()

        self.rows.add(int(0))
        self.rows.add(self.trueWidth - 1)
        self.columns.add(int(0))
        self.columns.add(self.trueLength - 1)

        # get the vertical border lines
        # step through each row
        for y in range(self.trueLength - 1):
            # step through each column on each row, excluding edges
            for x in range(self.trueWidth - 1):
                rgb = self.img.getpixel((x, y))
                rgbPrev = self.img.getpixel((x - 1, y))
                rgbNext = self.img.getpixel((x + 1, y))

                if rgb == self.borderColor and rgbPrev != self.borderColor and rgbNext != self.borderColor:
                    self.rows.add(int(x))

        # get the horizontal border lines
        # step through each column
        for x in range(self.trueWidth - 1):
            # step through each row on each column, excluding the edges
            for y in range(self.trueLength - 1):
                rgb = self.img.getpixel((x, y))
                rgbPrev = self.img.getpixel((x, y - 1))
                rgbNext = self.img.getpixel((x, y + 1))

                if(rgb == self.borderColor and rgbPrev != self.borderColor and rgbNext != self.borderColor):
                    self.columns.add(int(y))

        self.rows = sorted(self.rows)
        self.columns = sorted(self.columns)

    def writeNum(self, img, coord, num, color):
        font = ImageFont.truetype("calibri", self.approximateSqrSize[0] + 3)

        img.text(coord, str(num), color, font=font)

def main():
    imgPath = "test.png"

    if imgPath == "test.png":
        width = 36
        length = 45
    elif imgPath == "test2.png":
        width = 55
        length = 83
    elif imgPath == "test3.png":
        width = 72
        length = 70



    counter = PixelCounter(imgPath, width, length)    
    # counter.count()
    counter.sampleColors()
    print("test")


if __name__ == "__main__":
    main()



