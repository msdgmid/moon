import statistics
import sys
import time

from audioplayer import AudioPlayer
from navertts import NaverTTS

from src.upbit import Upbit
from statistics import stdev


def play(text):
    tts = NaverTTS(text)
    tts.save('alert.mp3')
    AudioPlayer('alert.mp3').play(block=True)


if __name__ == '__main__':
    access_key = '' # Upbit Access Key
    secret_key = '' # Upbit Secret Key
    upbit = Upbit(access_key, secret_key)

    # Init
    CANDLE_MIN_UNIT = 3
    MAX_COUNT = 200
    OUTLIER_COUNT = 25
    STDEV_RATE = 2.0

    markets = dict()
    for x in upbit.markets():
        if 'KRW' not in x.market():
            continue

        candles = upbit.candles(x.market())
        min_candles = candles.minute(unit=CANDLE_MIN_UNIT, count=MAX_COUNT)

        volumes = [y.candle_acc_trade_volume() for y in min_candles]
        sorted(volumes)

        markets[x.market()] = {
            'name': x.korean_name(),
            'caution': True if x.market_warning() == 'CAUTION' else False,
            'volume': volumes[OUTLIER_COUNT:len(volumes) - OUTLIER_COUNT],
            'price': 0
        }

        print('Market: {}, Std dev: {}'.format(x.market(), stdev(markets[x.market()]['volume'])))

    while True:
        for x in upbit.markets():
            if 'KRW' not in x.market():
                continue

            market = markets[x.market()]
            caution = True if x.market_warning() == 'CAUTION' else False

            if market['caution'] != caution:
                if caution:
                    play('{} 유의종목으로 지정되었습니다.'.format(market['name']))
                else:
                    play('{} 유의종목에서 해제되었습니다.'.format(market['name']))

            market['caution'] = caution

        for key, value in markets.items():
            candles = upbit.candles(key)
            min_candles = candles.minute(unit=CANDLE_MIN_UNIT)
            unit = min_candles[0]

            vol_list = value['volume']
            cur_vol = unit.candle_acc_trade_volume()
            len_vol = len(vol_list)

            prev_stdev_vol = stdev(vol_list)
            vol_list.append(cur_vol)
            cur_stdev_vol = stdev(vol_list)
            print('Market: {}, Cur: {}, Prev Std dev: {}, Cur Std dev: {}'.format(key, cur_vol, prev_stdev_vol,
                                                                                  cur_stdev_vol))

            if (STDEV_RATE * prev_stdev_vol) < cur_stdev_vol:
                play('{} 거래량이 급등하였습니다.'.format(value['name']))

            if len_vol > MAX_COUNT:
                sorted(vol_list)
                value['volume'] = vol_list[OUTLIER_COUNT:len_vol - OUTLIER_COUNT]
