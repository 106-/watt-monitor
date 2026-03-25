import math
import time

from gpiozero import MCP3008

resist = 460  # CTセンサに付けている負荷抵抗
rate = 3000  # CTセンサの変換比
max_voltage = 5.00  # 回路の最大電圧
sample_duration = 0.1  # サンプリング時間(秒) = 50Hzの5周期分
effective_voltage = 100  # 交流電源の実効電圧

# `pot.value`の値は0から1の範囲
pot = MCP3008(channel=0, max_voltage=max_voltage)

# 2.5Vに分圧しているので`pot.value`の平均は0.5になるはずだが, 実際には少しずれている.
# それがこの変数である.
bias = 0.492533


def power() -> float:
    """クランプ内に流れる電力を返す(交流なので負の値もありえる)"""
    # `pot.value`の取る値[0, +1]を[-0.5, +0.5]の範囲にしたあと,
    # 最大電圧(5.0V)をかけて電圧に変換する.
    voltage = (pot.value - bias) * max_voltage
    # オームの法則から, センサーに流れている電流を計算する.
    ampere = voltage / resist
    # CTセンサに流れている電流から, 観測対象の回路の電流を計算する.
    ampere_observe = ampere * rate
    # 電流*実効電圧で電力量を計算する.
    return ampere_observe * effective_voltage


def rms_power() -> float:
    """sample_duration秒間のサンプルを使ったRMS電力を返す"""
    samples = []
    deadline = time.monotonic() + sample_duration
    while time.monotonic() < deadline:
        samples.append(power() ** 2)
    return math.sqrt(sum(samples) / len(samples))


def rms_power_test() -> tuple[float, int]:
    """rms_powerと同じ計測を行い、(RMS電力, サンプル数)を返す"""
    samples = []
    deadline = time.monotonic() + sample_duration
    while time.monotonic() < deadline:
        samples.append(power() ** 2)
    return math.sqrt(sum(samples) / len(samples)), len(samples)
