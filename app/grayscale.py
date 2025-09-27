import cv2

class GrayScale:
    async def convert_image(image):
        # Load the image
        image_path = '1.jpg'  # Replace with your image filename if needed
        image = cv2.imread(image_path)
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply adaptive thresholding to highlight text while suppressing background noise
        binary_image = cv2.adaptiveThreshold(
            gray, 
            255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 
            15, 10
        )

        # Use morphological closing to further reduce noise if necessary
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cleaned_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

        # Save the result as "cleaned"
        cv2.imwrite('cleaned.jpg', cleaned_image)

        # Optional: Display the result (comment out if running in a non-GUI environment)
        # cv2.imshow('Cleaned Image', cleaned_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
