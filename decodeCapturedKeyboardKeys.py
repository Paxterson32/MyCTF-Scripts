# Credits to Odintheprotector

# Mapping between the hex values and the corresponding strings
usb_codes = {
        0x04:"aA", 0x05:"bB", 0x06:"cC", 0x07:"dD", 0x08:"eE", 0x09:"fF",
        0x0A:"gG", 0x0B:"hH", 0x0C:"iI", 0x0D:"jJ", 0x0E:"kK", 0x0F:"lL",
        0x10:"mM", 0x11:"nN", 0x12:"oO", 0x13:"pP", 0x14:"qQ", 0x15:"rR",
        0x16:"sS", 0x17:"tT", 0x18:"uU", 0x19:"vV", 0x1A:"wW", 0x1B:"xX",
        0x1C:"yY", 0x1D:"zZ", 0x1E:"1!", 0x1F:"2@", 0x20:"3#", 0x21:"4$",
        0x22:"5%", 0x23:"6^", 0x24:"7&", 0x25:"8*", 0x26:"9(", 0x27:"0)",
        0x2C:"  ", 0x2D:"-_", 0x2E:"=+", 0x2F:"[{", 0x30:"]}",  0x32:"#~",
        0x33:";:", 0x34:"'\"",  0x36:",<",  0x37:".>"
}

data = ''
# the characteres we are looking for are stored in the 3bytes ( Ex :  00 00 04 00 .. the third byte is 04 in hex)
for x in open("strings.txt","r").readlines():
        #convert third byte into int
        code = int(x[4:6],16)
        print(x[4:6]) # print the third byte
        if code == 0: # if the retrieved value is 0 in int then we move to the next line
                continue
        if code == 0x28:  # if we get 0x28, then it's the enter sign. We will display ENTER and move to the line in the display part
                print('ENTER!')
                print(data)
                data = '' # New data string will be made
                continue
        upper = 0
        if int(x[0:2],16) == 0x02 or int(x[0:2],16) == 0x20: # we will verify if the shift is pressed or capslock and if then, the upper variable will
                # be put to 1 in order to retrieve the upper corresponding character. 
                upper = 1
        data += usb_codes[code][upper]
print(data)
