class BarcodeImageGenerator:
    def generate_barcode_image(barcode, savePath):
        from PIL import Image, ImageDraw
        import constants

        im = Image.new('RGB', (len(barcode) * 2, constants.IMAGE_SIZE*constants.NUM_PROJECTIONS), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        px = 0
        for d in barcode:
            if d == 1:
                draw.rectangle((px, 0, px + 2, constants.IMAGE_SIZE*constants.NUM_PROJECTIONS), fill=(0, 0, 0))
            px += 2

        im.save(savePath, quality=100)
