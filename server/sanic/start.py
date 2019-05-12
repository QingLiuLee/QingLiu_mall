# -*- coding: utf-8 -*-
# @Time     : 4/24/19 9:58 AM
# @Author   : Lee才晓
# @Describe :

from system.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
