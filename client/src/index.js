import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter,Switch } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './reducer/store';

import App from './containers/App/App';
import 'antd/dist/antd.min.css';
import './assert/container.less';
import './assert/style.less';

ReactDOM.render(
    <Provider store={store}>
        <BrowserRouter>
            <Switch>
                <App />
            </Switch>
        </BrowserRouter>
    </Provider>,
    document.getElementById('root')
);