from PIL import Image, ImageFont, ImageDraw
import os
import re

class PixelCounter:
    def __init__(self, imgPath, saveFilePath,width, length, threshold, ignoredValues) -> None:
        self.img = Image.open(imgPath)
        self.img = self.img.convert("RGB")
        self.borderColor = self.img.getpixel((0, 0))
        self.trueWidth, self.trueLength = self.img.size
        self.counts = []
        self.drawThreshold = threshold
        self.filename = re.search("[^/]+$", imgPath).group().split(".")
        self.saveFilePath = saveFilePath
        self.topIgnored, self.bottomIgnored, self.leftIgnored, self.rightIgnored = ignoredValues

        # These variables help with choosing a font size
        self.width = width
        self.length = length
        self.approximateSqrSize = ((self.trueWidth - 1) // self.width , (self.trueLength - 1) // self.length)
        
        self.sampleColors()

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

        # remove columns based on ignored numbers
        for x in range(self.topIgnored):
            self.columns.pop(0)
        for x in range(self.bottomIgnored):
            # self.columns.pop(len(self.columns) - 1)
            self.columns.pop()
        for x in range(self.leftIgnored):
            self.rows.pop(0)
        for x in range(self.rightIgnored):
            # self.rows.pop(len(self.rows) - 1)
            self.rows.pop()

    def count(self):
        img_editable = ImageDraw.Draw(self.img)

        # step through each row
        # counting and drawing the adjacent colors in each row
        for y in range(0, len(self.columns) - 1):
            rowCounts = []
            rgbPrev = self.img.getpixel((self.rows[0] + 1, self.columns[y] + 1))
            drawX = 0
            count = 1

            # step through each column
            for x in range(1, len(self.rows) - 1):
                rgb = self.img.getpixel((self.rows[x] + 1, self.columns[y] + 1))

                if rgb == rgbPrev:
                    count += 1
                else:
                    if(count >= self.drawThreshold):
                        self.writeNum(img_editable, drawX, y, count, rgbPrev)

                    rowCounts.append((rgbPrev, count))
                    rgbPrev = rgb
                    drawX = x
                    count = 1

            if(count >= self.drawThreshold):
                self.writeNum(img_editable, drawX, y, count, rgbPrev)

            rowCounts.append((rgbPrev, count))

            self.counts.append(rowCounts)
        self.img.save(f"{self.saveFilePath}{self.filename[0]}.{self.filename[1]}")

    def writeNum(self, img, x, y, count, rgb):
        countStr = str(count)
        font = ImageFont.truetype("calibri", self.approximateSqrSize[0] + 3)
        if rgb == (0, 0, 0):
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)

        for num in countStr:
            img.text((self.rows[x] + 3, self.columns[y] + 1), str(num), color, font=font)
            x += 1

# eva: 36, 45
# fish: 72, 70
# lady: 55, 83
