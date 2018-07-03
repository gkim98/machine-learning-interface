import base64
import pandas as pd
import io

# processes data from uploader then performs action on it
def parse_contents(contents, filename, date, action):
    if contents is None : return action(None)
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)

    return action(df)