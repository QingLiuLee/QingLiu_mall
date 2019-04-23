# QingLiu
青榴社区

> redux
```
    yarn add redux react-redux redux-thunk --save
    yarn add redux-logger --dev
           redux : 是把它当成一个本地数据库使用，
     react-redux : 帮助你完成数据订阅
     redux-thunk : 可以放你实现异步action
    redux-logger : redux的日志中间件

    import { Provider } from 'react-redux'
    import { createStore, applyMiddleware, compose } from 'redux';
    import thunk from 'redux-thunk';
    //多个redux.js
    import reducer from './reducer/combineReducers';

    const store = createStore(reducer,compose(
        applyMiddleware(thunk),
        window.devToolsExtension ? window.devToolsExtension():f=>f
    ));

    ReactDOM.render(
        <Provider store={store}>
            ...
        </Provider>,
        document.getElementById('root')
    );

    err:__WEBPACK_IMPORTED_MODULE_0_react___default.a.createContext is not a function
        降低react-redux版本 :"^5.0.7"

    使用：
        import { connect } from 'react-redux';
        import {getLoginData} from '../../reducer/login.redux';
        @connect(
            state=>state.login,
            {getLoginData}
        )
```

> clean-webpack-plugin
```
    yarn add clean-webpack-plugin --dev

    onst CleanWebpackPlugin = require('clean-webpack-plugin');
    const webpackConfig = {
        plugins: [
            /**
             * All files inside webpack's output.path directory will be removed once, but the
             * directory itself will not be. If using webpack 4+'s default configuration,
             * everything under <PROJECT_DIR>/dist/ will be removed.
             * Use cleanOnceBeforeBuildPatterns to override this behavior.
             *
             * During rebuilds, all webpack assets that are not used anymore
             * will be removed automatically.
             *
             * See `Options and Defaults` for for information
             */
            new CleanWebpackPlugin(),
        ],
    };
```