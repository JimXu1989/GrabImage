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
# resDict= { "ImNum", "ImReadFlag", "ComponentExFlag", "TarBoxPts", "AimBoxXcnt","AimBoxYcnt",
#            "TargetBoxStatus", "AimBoxStatus", "ImgSatisfiedFlag","ContourExFlag","Diameter",
#            "ContourPointX", "ContourPointY" };
# 变量定义
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


def decode_result_state(case, resDict):
    # 定义函数返回值
    TarBox = resDict.get('TarBoxPts')
    AimBoxPointX = resDict.get('AimBoxXcnt')
    AimBoxPointY = resDict.get('AimBoxYcnt')
    shortD = 0  # 检尺径
    contourX = 0  # 轮廓点X方向坐标
    contourY = 0  # 轮廓点Y方向坐标
    LongD = 0
    SlopeAng = 0
    SensorD = 0

    if case == [0, 0]:
        outStateCode = '00'  # 组件状态正常，满足测量要求
        isContourExist = resDict.get('ContourExFlag')
        if isContourExist == '1':
            shortD = resDict.get('Diameter')  # 检尺径
            contourX = resDict.get('ContourPointX')  # 轮廓点X方向坐标
            contourY = resDict.get('ContourPointY')  # 轮廓点Y方向坐标
            LongD = resDict.get('LongDiameter')      # 长径
            SlopeAng = resDict.get('SlopeAngle')     # 传感器测量倾角
            SensorD = resDict.get('SensorDist ')     # 传感器测量距离
            outCurrState = '测量成功'
            # print(outCurrState)
        else:
            outCurrState = '原木轮廓提取失败!'
            # print(outCurrState)
    elif case == [0, 1]:
        outStateCode = '01'  # 未发现目标框
        outCurrState = '未发现原木!'
    elif case == [0, 2]:
        outStateCode = '02'  # 未发现瞄准框
        outCurrState = '未发现瞄准框!'
    elif case == [0, 3]:
        outStateCode = '03'  # 测量倾角过大
        outCurrState = '测量设备倾角过大!'
    elif case == [1, 1]:
        outStateCode = '11'  # 测量设备距离目标太远
        outCurrState = '测量设备离目标太远!'
    elif case == [1, 2]:
        outStateCode = '12'  # 测量设备距离目标太近
        outCurrState = '测量设备离目标太近!'
    elif case == [1, 3]:
        outStateCode = '13'  # 目标上偏
        outCurrState = '测量设备上偏!'
    elif case == [1, 4]:
        outStateCode = '14'  # 目标下偏
        outCurrState = '测量设备下偏!'
    elif case == [1, 5]:
        outStateCode = '15'  # 目标左偏
        outCurrState = '测量设备左偏!'
    elif case == [1, 6]:
        outStateCode = '16'  # 目标右偏
        outCurrState = '测量设备右偏!'
    elif case == [2, 1]:
        outStateCode = '21'  # 传感器距离目标太远(瞄准框太大)
        outCurrState = '瞄准框太远!'
    elif case == [2, 2]:
        outStateCode = '22'  # 传感器距离目标太近(瞄准框太小)
        outCurrState = '瞄准框太近!'
    elif case == [2, 3]:
        outStateCode = '23'  # 瞄准框上偏
        outCurrState = '瞄准框上偏!'
    elif case == [2, 4]:
        outStateCode = '24'  # 瞄准框下偏
        outCurrState = '瞄准框下偏!'
    elif case == [2, 5]:
        outStateCode = '25'  # 瞄准框左偏
        outCurrState = '瞄准框左偏!'
    elif case == [2, 6]:  # 瞄准框左偏
        outStateCode = '26'
        outCurrState = '瞄准框右偏!'
    else:
        outStateCode = 'xxx'
        outCurrState = '未知错误！'
    return [outCurrState, outStateCode, TarBox, AimBoxPointX, AimBoxPointY,
            shortD, contourX, contourY, LongD, SlopeAng, SensorD]


# 获取组件状态，在组件状态满足测量要求时返回目标的检尺径，轮廓点坐标
def check_resDict(clientImID, resDict):
    # 定义函数返回值
    outCurrState = 0
    outStateCode = 'xxx'
    shortD = 0  # 检尺径
    contourX = 0  # 轮廓点X方向坐标
    contourY = 0  # 轮廓点Y方向坐标
    LongD = 0
    SlopeAng = 0
    SensorD = 0
    # 调用读文本文件函数
    # 获得当前文件中指定项
    TarBox = resDict.get('TarBoxPts')
    AimBoxPointX = resDict.get('AimBoxXcnt')
    AimBoxPointY = resDict.get('AimBoxYcnt')
    # 生成缺省返回值
    resList = [outCurrState, outStateCode, TarBox, AimBoxPointX, AimBoxPointY, shortD,
               contourX, contourY, LongD, SlopeAng, SensorD]

    # 判断字典类型数据长度是否满足要求
    lenDict = len(resDict)
    if lenDict == 21:
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
                resList = decode_result_state(outList, resDict)
                # print(resList[0])
            else:
                outCurrState = '服务端与客户端图像ID号不同'
                resList[0] = outCurrState
                # print(resList[0])
        elif ImLoadFlag == '0':
            outCurrState = '服务端读图失败'
            resList[0] = outCurrState
            # print(resList[0])
        elif ImLoadFlag == '11':
            outCurrState = '服务端开启保存图像模式'
            resList[0] = outCurrState
            # print(resList[0])
        else:
            outCurrState = '图像读取标记项数值发生错误！'
            resList[0] = outCurrState
            # print(resList[0])
    elif lenDict == 0:
        outCurrState = '未发现文本文件！'
        resList[0] = outCurrState
        # print(resList[0])
    else:
        outCurrState = '文本文件格式错误！'
        resList[0] = outCurrState
        # print(resList[0])
    # 返回值说明：当前测量状态、测量状态编号、目标框坐标数组、瞄准框X坐标数组、瞄准框Y坐标数组、检尺径、轮廓点坐标X、轮廓点坐标Y、
    #            长径、测量倾角、测量距离
    return resList

currImageID = '1596185503390'  # 采集装置采集获得的图像名
if __name__ == "__main__":
    resList = check_resDict(currImageID)
    time.sleep(0.5)
