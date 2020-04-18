import cv2

def get_user_key_code(title):
    img = cv2.imread("test.jpg")
    cv2.imshow(title, img)
    user_input = cv2.waitKey(0)
    return user_input

if __name__ == "__main__":
    title = "Enter left arrow key" 
    print(title)
    code = get_user_key_code(title)
    print("Code for left key: ", code)

    title = "Enter right arrow key" 
    print(title)
    code = get_user_key_code(title)
    print("Code for right key: ", code)
