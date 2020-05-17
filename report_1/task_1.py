import json
import os
from dotenv import load_dotenv

import gspread
import matplotlib.pyplot as plt
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials


class Main:
    def __init__(self, w0, w1, l, inputs):
        self.x0 = 1
        self.w0, self.w1 = w0, w1
        self.l = l
        self.inputs = inputs
        self.flag = False
        self.count = 0
        self.update_count = 1
        self.row = 3
        self.save_data()
    
    def save_data(self):
        load_dotenv('./.env')
        file_name = 'prismatic-petal-198815-3422944891c6.json'
        json_open = open('./prismatic-petal-198815-3422944891c6.json', 'r')
        json_load = json.load(json_open)
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
        gc = gspread.authorize(credentials)
        SPREADSHEET_KEY = os.environ['SPREADSHEET_KEY']
        self.worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

    def show(self, value):
        x = np.arange(-2.5, 2.5, 0.1)
        y = [0] * 50

        plt.plot(x, y)
        plt.plot(y, x)

        plt.plot([value]*50, x, 'o', color='green', ms=3)
        plt.plot(1, 0, 'o', color='red')
        plt.plot(0.2, 0, 'o', color='red')
        plt.plot(-0.1, 0, 'o', color='red')
        plt.plot(-2, 0, 'o', color='red')
        # plt.savefig('./image/image_{}.png'.format(self.count))
        
        self.count += 1

        plt.show()
    
    def cal(self, value):
        return self.w0 * self.x0 + self.w1 * value
    
    def make(self, value):
        print("値と計算結果", value, self.cal(value))
        caled_value = self.cal(value)
        # 重みベクトルの更新
        if value * caled_value < 0:
            self.w0 += -self.l * self.x0 if value < 0 else self.l * self.x0
            self.w1 += -self.l * value if value < 0 else self.l * value
            print('update', self.w0, self.w1)
            self.worksheet.update_cell(self.row, 1, '重み更新({}回目)'.format(self.update_count))
            self.worksheet.update_cell(self.row, 2, self.w0)
            self.worksheet.update_cell(self.row, 3, self.w1)
            self.worksheet.update_cell(self.row, 4, '{}x {}'.format(self.w0, ('+{}'.format(self.w1) if self.w1 >= 0 else self.w1)))
            self.update_count += 1
            self.row += 1
            return False
        return True

    def main(self):
        self.worksheet.update_cell(2, 2, self.w0)
        self.worksheet.update_cell(2, 3, self.w1)
        self.worksheet.update_cell(2, 4, '{}x {}'.format(self.w0, ('+{}'.format(self.w1) if self.w1 >= 0 else self.w1)))
        print('initial', self.w0, self.w1)
        while True:
            flags = []
            for item in self.inputs:
                flag = self.make(item)
                flags.append(flag)
            if all(flags):
                break
        print('hello')

    def make_gif(self):
        from PIL import Image
        import glob

        files = sorted(glob.glob('./image/*.png'))
        images = list(map(lambda file: Image.open(file), files))
        images[0].save('out.gif', save_all=True, append_images=images[1:], duration=400, loop=0)

if __name__ == '__main__':
    w0, w1 = 0.4, -0.4
    l = 0.3
    inputs = [1, 0.2, -0.1, -2.0]
    # w0, w1 = 0.2, 0.3
    # l = 0.5
    # inputs = [1.2, 0.5, -0.2, -1.5]
    main = Main(w0, w1, l, inputs)
    main.main()
    print(main.w0, main.w1)
    # main.make_gif()
