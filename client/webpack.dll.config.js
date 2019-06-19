const webpack = require('webpack');
const path = require('path');

//判断当前运行环境是开发模式还是生产模式
const nodeEnv = process.env.NODE_ENV || "development";
// 当前运行环境是生产环境
const isPro = nodeEnv === "production";
console.log("当前运行环境：", isPro ? "production" : "development");

let dir = "public/dll";
if (isPro) {
    dir = "dist/dll";
}

const vendors = [
    'react',
    'react-dom',
    'react-router',
    'react-router-dom',
    'redux',
    'react-redux',
    'redux-thunk',
    'antd'

    // ...其它库
];

module.exports = {
    // context:path.resolve(__dirname, 'src'),
    output: {
        path:path.join(__dirname, dir),
        filename: 'dll.js',
        library: 'dll'
    },
    entry: {
        dll: vendors,
    },
    plugins: [
        new webpack.DllPlugin({
            context:__dirname,
            path: path.join(__dirname, dir + '/manifest.json'),
            name: 'dll'
        })
    ],
};
