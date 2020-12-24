import requests


def visit(method, url,
          params=None,
          data=None,
          json=None,
          **kwargs):
    res = requests.request(method.lower(), url, params=params, data=data, json=json, **kwargs)
    try:
        return res.json()
    except Exception as e:
        raise e


if __name__ == '__main__':
    pass
