import time, yaml
from datetime import datetime
from display import Display
from sources.yahoo import fetch as fetch_stock
from sources.coingecko import fetch as fetch_crypto


FETCHERS = {
'stock': fetch_stock,
'crypto': fetch_crypto,
}


def run():
    with open('config.yaml') as f:
    cfg = yaml.safe_load(f)


    disp = Display(rotation=cfg['display'].get('rotation', 0))
    refresh_s = int(cfg['display'].get('refresh_seconds', 60))
    invert_down = bool(cfg['display'].get('invert_down', True))


    symbols = cfg['symbols']
    try:
        disp.clear()
        while True:
            for item in symbols:
                f = FETCHERS[item['type']]
                data = f(item['symbol'])
                disp.draw_ticker(
                label=item.get('label', data['symbol']),
                price=data['price'],
                change_pct=data['change_pct'],
                ts=datetime.now(),
                invert_down=invert_down,
                )
            time.sleep(refresh_s)
    except KeyboardInterrupt:
        disp.sleep()


if __name__ == '__main__':
    run()