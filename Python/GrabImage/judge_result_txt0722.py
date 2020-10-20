""" 算法说明
    由文本文件（resFile.txt）读取测量结果，由测量结果判断测量任务是否完成，具体判断过程如下：
    step1 - 打开resFile.txt文本文件。若成功，则流程转到step2；否则，返回。
    step2 - 将文本文件各行内容装订成字典类型数据（resDict）。若该字典变量长度满足要求，则流程转到step3；否则，返回
    step3 - 判断文本文件中图像ID是否等于采集装置中图像的ID。若相等，流程转到step4；否则，返回。
    step4 - 判断实际边框数组与标准边框数组值是否相等。若相等，流程转到step5；否则，流程转到step7。
    step5 - 首先判断目标框状态（TarBoxState=[0,0,0,0,0,0], 各元素依次表示：远、近、上偏、下偏、左偏、右偏。
            其中"0"表示不偏，“1”表示偏移）；其次，判断瞄准框状态（AimBoxState, 各元素含义同上）。该步返回值：outList
            可能的取值为[1,x]、[2,x]、[0,0], 其中[0,0]表示目标框与瞄准框位置都正确，[1,x]表示目标框发生偏移，且x向
            发生偏移（x=1、2、3、4、5、6中的一个，对应方向为：远、近、上、下、左、右）。[2,x]表示瞄准框发生偏移，x含义同上。
            若返回值outList=[0,0],则流程转到step6；否则，返回。
    step6 - 判断轮廓提取是否成功。若成功，则返回检尺径实际值；否则，检尺径等于零。
    step7 - 接step4流程，确定目标框、瞄准框、倾角过大是否存在。若目标框不存在，则返回值outList=[0,1]；
            若瞄标框不存在，则返回值outList=[0,2]；若倾角过大，则返回值outList=[0,3]
    备注：当轮廓提取成功后，算法还可以返回轮廓点的X、Y坐标值。
    说明：注释中所提到的 “组件” 由目标框、瞄准框、倾角三者构成

    # This Algorithm is designed by Xu Min in 2020/7/20
"""
import time

# resDict参考键
# resDict= { "ImNum", "ImReadFlag", "ComponentExFlag", "TargetBoxStatus", "AimBoxStatus", "ImgSatisfiedFlag",
#            "ContourExFlag","Diameter", "ContourPointX", "ContourPointY" };
# 变量定义
currImageID = '1576229328195.bmp'  # 采集装置采集获得的图像名
BoxStdFlag = '1,1,0'  # 默认组件存在标记


# 读取文本文件，并输出字典类型数据
def read_txt_out_dict(filePath='./resFile.txt'):
    try:
        file = open(filePath).read().strip().split('\n')
        resDict = {}
        for line in file:
            currLine = line.strip().split(':')
            if len(currLine) == 2:
                currDict = {currLine[0]: currLine[1]}
                resDict.update(currDict)
    except IOError:
        resDict = {}
    return resDict


# 判断各组件是否存在，以及各组件位置是否正确
# 返回值outList说明：outList = [0, 0]表示各组件存在且位置满足要求
#                   outList = [0, 1]表示未发现目标框
#                   outList = [0, 2]表示未发现瞄准框
#                   outList = [0, 3]表示未测量倾角过大
#                   outList = [1, x]表示目标框偏移，具体偏移方向参考x，x取1、2、3、4、5、6中的一个，表示远、近、上、下、左、右
#                   outList = [2, x]表示瞄准框偏移，具体偏移方向参考x，x同上。
def encode_result_state(boxExistFlag, tarBoxState, aimBoxState):
    # 若框组件与标准值相同, 则首先判断目标框位置是否正确，然后判断瞄准框是否正确
    if boxExistFlag == BoxStdFlag:
        # 判断目标框（tarBoxState）位置是否正确, 正确值为tarBoxState = [0,0,0,0,0,0]
        max1 = max(tarBoxState)
        if max1 == 0:  # 目标框位置正确
            # 判断目标框（aimBoxState）位置是否正确, 正确值为aimBoxState = [0,0,0,0,0,0]
            max2 = max(tarBoxState)
            if max2 == 0:
                outList = [0, 0]
            else:  # max2 ==1
                max2_idx = aimBoxState.index(max2)  # max2 在数组aimBoxState中的索引值
                oneIdx = max2_idx + 1
                outList = [2, oneIdx]
        else:  # max1 ==1
            max1_idx = tarBoxState.index(max1)  # max1 在 tarBoxState中的索引号
            oneIdx = max1_idx + 1
            outList = [1, oneIdx]
        return outList
    else:  # 框组件与标准值不同(确定目标框、瞄准框、倾角过大中的哪个发生)
        if boxExistFlag == '0,0,0':
            outList = [0, 1]
        elif boxExistFlag == '1,0,0':
            outList = [0, 2]
        elif boxExistFlag == '1,1,1':
            outList = [0, 3]
        else:
            outList = []
        return outList


def decode_result_state(case):
    if case == [0, 0]:
        outState = '00'  # 组件状态正常，满足测量要求
    elif case == [0, 1]:
        outState = '01'  # 未发现目标框
    elif case == [0, 2]:
        outState = '02'  # 未发现瞄准框
    elif case == [0, 3]:
        outState = '03'  # 测量倾角过大
    elif case == [1, 1]:
        outState = '11'  # 传感器距离目标太远
    elif case == [1, 2]:
        outState = '12'  # 传感器距离目标太近
    elif case == [1, 3]:
        outState = '13'  # 目标上偏
    elif case == [1, 4]:
        outState = '14'  # 目标下偏
    elif case == [1, 5]:
        outState = '15'  # 目标左偏
    elif case == [1, 6]:
        outState = '16'  # 目标右偏
    elif case == [2, 1]:
        outState = '21'  # 传感器距离目标太远(瞄准框太大)
    elif case == [2, 2]:
        outState = '22'  # 传感器距离目标太近(瞄准框太小)
    elif case == [2, 3]:
        outState = '23'  # 瞄准框上偏
    elif case == [2, 4]:
        outState = '24'  # 瞄准框下偏
    elif case == [2, 5]:
        outState = '25'  # 瞄准框左偏
    elif case == [2, 6]:
        outState = '26'
    else:
        outState = []
    return outState


# 获取组件状态，在组件状态满足测量要求时返回目标的检尺径，轮廓点坐标
def main(clientImID):
    # 定义函数返回值
    outStateCode = []
    shortDiameter = 0  # 检尺径
    contourX = 0  # 轮廓点X方向坐标
    contourY = 0  # 轮廓点Y方向坐标

    # 调用读文本文件函数
    resDict = read_txt_out_dict()

    # 判断字典类型数据长度是否满足要求
    lenDict = len(resDict)
    if lenDict == 10:
        # 判断Server端工作模式：存图像模式、图像处理模式
        ImLoadFlag = resDict.get('ImReadFlag')
        if ImLoadFlag == '1':
            ImageID = resDict.get('ImNum')  # 获取字典中图像的ID号
            # 判断resFile中图像名与采集装置中保存的图像名是否相同
            if ImageID == clientImID:
                BoxExistFlag = resDict.get('ComponentExFlag')  # 获取组件存在标记
                strTarBoxState = resDict.get('TargetBoxStatus')  # 获取目标框位置状态值
                TarBoxState = strTarBoxState.split(',')  # 将字符串按要求分割成字符数组
                TarBoxState = [int(x) for x in TarBoxState]  # 字符数组转成整形数组
                strAimBoxState = resDict.get('AimBoxStatus')  # 获取瞄准框位置状态值
                AimBoxState = strAimBoxState.split(',')  # 将字符串按要求分割成字符数组
                AimBoxState = [int(x) for x in AimBoxState]  # 字符数组转成整形数组
                # 调用组件状态编码函数
                outList = encode_result_state(BoxExistFlag, TarBoxState, AimBoxState)
                # 调用组件状态解码函数
                outStateCode = decode_result_state(outList)
                # 组件状态正确时，提取目标检尺径，以及轮廓点坐标
                if outStateCode == '00':
                    isContourExist = resDict.get('ContourExFlag')
                    if isContourExist == '1':
                        shortDiameter = resDict.get('Diameter')  # 检尺径
                        contourX = resDict.get('ContourPointX')  # 轮廓点X方向坐标
                        contourY = resDict.get('ContourPointY')  # 轮廓点Y方向坐标
                        outCurrState = 'Measurement is success'
                        print(outCurrState)
                    else:
                        outCurrState = 'the contour is not exist'
                        print(outCurrState)

                else:
                    outCurrState = 'Component state is wrong'
                    print(outCurrState)

            else:
                outCurrState = 'Server-Client image names are different'
                print(outCurrState)

        elif ImLoadFlag == '0':
            outCurrState = 'Server is failed to read images'
            print(outCurrState)

        elif ImLoadFlag == '11':
            outCurrState = 'Saving images mode is on'
            print(outCurrState)

        else:
            outCurrState = 'Item "ImReadFlag" in the file is wrong!'
            print(outCurrState)

    elif lenDict == 0:
        outCurrState = 'The file is not exist'
        print(outCurrState)

    else:
        outCurrState = 'File formal is wrong'
        print(outCurrState)
    # 返回值说明：传感器状态、状态编号、检尺径、轮廓点坐标X、轮廓点坐标Y
    return outCurrState, outStateCode, shortDiameter, contourX, contourY


def check_resDict(clientImID):
    # 定义函数返回值
    outStateCode = []
    shortDiameter = 0  # 检尺径
    contourX = 0  # 轮廓点X方向坐标
    contourY = 0  # 轮廓点Y方向坐标

    # 调用读文本文件函数
    resDict = read_txt_out_dict()

    # 判断字典类型数据长度是否满足要求
    lenDict = len(resDict)
    if lenDict == 10:
        # 判断Server端工作模式：存图像模式、图像处理模式
        ImLoadFlag = resDict.get('ImReadFlag')
        if ImLoadFlag == '1':
            ImageID = resDict.get('ImNum')  # 获取字典中图像的ID号
            # 判断resFile中图像名与采集装置中保存的图像名是否相同
            if ImageID == clientImID:
                BoxExistFlag = resDict.get('ComponentExFlag')  # 获取组件存在标记
                strTarBoxState = resDict.get('TargetBoxStatus')  # 获取目标框位置状态值
                TarBoxState = strTarBoxState.split(',')  # 将字符串按要求分割成字符数组
                TarBoxState = [int(x) for x in TarBoxState]  # 字符数组转成整形数组
                strAimBoxState = resDict.get('AimBoxStatus')  # 获取瞄准框位置状态值
                AimBoxState = strAimBoxState.split(',')  # 将字符串按要求分割成字符数组
                AimBoxState = [int(x) for x in AimBoxState]  # 字符数组转成整形数组
                # 调用组件状态编码函数
                outList = encode_result_state(BoxExistFlag, TarBoxState, AimBoxState)
                # 调用组件状态解码函数
                outStateCode = decode_result_state(outList)
                # 组件状态正确时，提取目标检尺径，以及轮廓点坐标
                if outStateCode == '00':
                    isContourExist = resDict.get('ContourExFlag')
                    if isContourExist == '1':
                        shortDiameter = resDict.get('Diameter')  # 检尺径
                        contourX = resDict.get('ContourPointX')  # 轮廓点X方向坐标
                        contourY = resDict.get('ContourPointY')  # 轮廓点Y方向坐标
                        outCurrState = 'Measurement is success'
                        print(outCurrState)
                    else:
                        outCurrState = 'the contour is not exist'
                        print(outCurrState)

                else:
                    outCurrState = 'Component state is wrong'
                    print(outCurrState)

            else:
                outCurrState = 'Server-Client image names are different'
                print(outCurrState)

        elif ImLoadFlag == '0':
            outCurrState = 'Server is failed to read images'
            print(outCurrState)

        elif ImLoadFlag == '11':
            outCurrState = 'Saving images mode is on'
            print(outCurrState)

        else:
            outCurrState = 'Item "ImReadFlag" in the file is wrong!'
            print(outCurrState)

    elif lenDict == 0:
        outCurrState = 'The file is not exist'
        print(outCurrState)

    else:
        outCurrState = 'File formal is wrong'
        print(outCurrState)
    # 返回值说明：传感器状态、状态编号、检尺径、轮廓点坐标X、轮廓点坐标Y
    return outCurrState, outStateCode, shortDiameter, contourX, contourY


if __name__ == "__main__":
    resList = main(currImageID)
    time.sleep(1)
