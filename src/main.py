import datetime
import json

MAX_FLOOR = 10
FEE_PARK = 1

# 주차장 주차 현황 출력
def print_park_info():
    print(f"{"=" * 20} parking lot information {"=" * 20}")
    for i in range(MAX_FLOOR):
        print(f"{MAX_FLOOR - i}층:\t", end="")
        for j in range(10):
            if j == 9:
                print("[ ]" if parking_lot_info[i][j] == 0 else "[X]")
            else:
                print("[ ]" if parking_lot_info[i][j] == 0 else "[X]", end=" ")
    print()

# 정기 등록 차량 출력
def print_registered_vehicle_info():
    print(f"{"=" * 20} registered vehicle information {"=" * 20}")
    print(json.dumps(registered_vehicle_info, indent=4), end="\n\n")

# 빈 주차장 자리 찾기
def get_parking_position():
    flag = False

    for i in range(MAX_FLOOR - 1, -1, -1):
        for j in range(10):
            if parking_lot_info[i][j] == 0:
                flag = True
                break
        if flag:
            break

    return (i, j)


# 주차장 정보 (0: 빔, 1: 참)
parking_lot_info = [
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 1, 0],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 1]
]

# 주차장에 들어온 차량 정보
parked_vehicle_info = dict()

# 정기 등록 차량 정보
registered_vehicle_info = {
    "1234": 20,
    "4567": 30,
    "3682": 40,
    "4482": 50
}

# 처음 시작 주차장 정보, 정기 등록 차량 출력을 위한 작업
parking_lot_flag = True
registered_vehicle_flag = True

while True:
    if parking_lot_flag:
        parking_lot_flag = False
        print_park_info()

    if registered_vehicle_flag:
        registered_vehicle_flag = False
        print_registered_vehicle_info()

    command = input("Enter command (\"exit\": exit | \"1\": vehicle in | \"2\": vehicle out | \"3\": add registered vehicle | \"4\": delete registered vehicle) | \"5\": read parked vehicle info | \"6\": add parking ticket: ")

    match command:
        # exit은 exit
        case "exit":
            break
        # 1은 차량 들어감
        case "1":
            car_num = input("Enter your car number: ")
            enter_time = datetime.datetime.now()
            parking_floor, parking_num = get_parking_position()

            print(f"{MAX_FLOOR - parking_floor} floor - {parking_num + 1} is empty. I'll park your vehicle \"{MAX_FLOOR - parking_floor} floor - {parking_num + 1}\"")

            parking_lot_info[parking_floor][parking_num] = 1

            car_type = input("Enter car type (electric, gasoline): ")

            parked_vehicle_info[car_num] = {"entertime": enter_time, "floor": parking_floor, "num": parking_num, "cartype": car_type, "parkingticket": False}

            parking_lot_flag = True
        # 2는 차량 나감
        case "2":
            car_num = input("Enter your car number: ")

            cur_vehicle_info = parked_vehicle_info.pop(car_num)

            parking_lot_info[cur_vehicle_info["floor"]
                             ][cur_vehicle_info["num"]] = 0

            parking_time = datetime.datetime.now(
            ) - cur_vehicle_info["entertime"]

            if cur_vehicle_info["parkingticket"]:
                if parking_time.total_seconds() > 20:
                    parking_senconds = parking_time.total_seconds() - 20
                else:
                    parking_senconds = 0
            else:
                parking_senconds = parking_time.total_seconds()
                if parking_senconds < 5:
                    parking_senconds = 0

            total_fee = parking_senconds * FEE_PARK

            if car_num in registered_vehicle_info:
                total_fee = total_fee * \
                    (100 - registered_vehicle_info[car_num]) / 100

            if cur_vehicle_info["cartype"] == "electric":
                total_fee = total_fee * 80 / 100

            print(f"{car_num} | total fee: {total_fee}")

            parking_lot_flag = True
        # 3은 정기 차량 등록
        case "3":
            car_num = input("Enter your car number: ")
            discount_rate = int(input("Enter discount rate(%): "))

            registered_vehicle_info[car_num] = discount_rate

            registered_vehicle_flag = True
        # 4는 정기 차량 삭제
        case "4":
            car_num = input("Enter your car number: ")

            registered_vehicle_info.pop(car_num)

            registered_vehicle_flag = True
        # 5는 들어온 차량 정보 출력
        case "5":
            print(f"parked vehicle info: {parked_vehicle_info}", end="\n\n")
        # 6은 주차권 등록
        case "6":
            car_num = input("Enter your car number: ")
            parked_vehicle_info[car_num]["parkingticket"] = True
