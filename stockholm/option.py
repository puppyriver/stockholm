import argparse 
import datetime

def get_date_str(offset):
    if(offset is None):
        offset = 0
    date_str = (datetime.datetime.today() + datetime.timedelta(days=offset)).strftime("%Y-%m-%d")
    return date_str

_default = dict(
    reload_data = 'Y',
    gen_portfolio = 'Y',
    output_type = 'json',
    test_date_range = 60,
    start_date = get_date_str(-100),
    end_date = get_date_str(None),
    target_date = get_date_str(None),
    store_path = 'USER_HOME/tmp/stockholm_export'
    )

parser = argparse.ArgumentParser(description='A stock crawler and portfolio testing framework.') 

parser.add_argument('--reload', type=str, default=_default['reload_data'], dest='reload_data', help='Reload the stock data or not, Default: %s' % _default['reload_data'])

parser.add_argument('--portfolio', type=str, default=_default['gen_portfolio'], dest='gen_portfolio', help='Generate the portfolio or not, Default: %s' % _default['gen_portfolio'])

parser.add_argument('--output', type=str, default=_default['output_type'], dest='output_type', help='Data output type, Default: %s' % _default['output_type'])

parser.add_argument('--testrange', type=int, default=_default['test_date_range'], dest='test_date_range', help='Test date range(days): %s' % _default['test_date_range'])

parser.add_argument('--startdate', type=str, default=_default['start_date'], dest='start_date', help='Data loading start date, Default: %s' % _default['start_date'])

parser.add_argument('--enddate', type=str, default=_default['end_date'], dest='end_date', help='Data loading end date, Default: %s' % _default['end_date'])

parser.add_argument('--targetdate', type=str, default=_default['target_date'], dest='target_date', help='Portfolio generating target date, Default: %s' % _default['target_date'])

parser.add_argument('--storepath', type=str, default=_default['store_path'], dest='store_path', help='Data file store path, Default: %s' % _default['store_path'])

## parser.add_argument('--enddate', type=str, required=True, default=_default['end_date'], dest='end_date', help='Data loading end date, Default: %s' % _default['end_date'])


def main():
    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()