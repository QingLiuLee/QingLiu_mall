const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const OpenBrowserPlugin  = require('open-browser-webpack-plugin');
// const CleanWebpackPlugin = require('clean-webpack-plugin');

//判断当前运行环境是开发模式还是生产模式
const nodeEnv = process.env.NODE_ENV || "development";
// 当前运行环境是生产环境
const isPro = nodeEnv === "production";

console.log("当前运行环境：", isPro ? "production" : "development");

let dir = "build";
if (isPro) {
    dir = "dist";
}

//插件css
const comPlugInCss = new ExtractTextPlugin({
    filename:'assert/css/comPlugInCss.css',
    allChunks:true
});
const styleCss = new ExtractTextPlugin({
    filename:'assert/css/app.css',
    allChunks:true
});

module.exports = {
    context:path.resolve(__dirname, '.'),
    devtool: isPro ? 'none' : 'cheap-module-source-map',  //设置本地源代码
    entry: {
        app: './src/index.js',  //入口
    },
    // 根据运行模式改变输出方式
    output: isPro ? {
        path: path.join(__dirname, dir),
        filename: "js/[name].[chunkhash:5].js",
        publicPath: "./",
        chunkFilename: "js/chunk/[id].[chunkhash:5].js"
    } : {
        path: path.join(__dirname, dir),
        publicPath: "/",
        filename: 'assert/js/[name].js',
    },
    module: {
        rules: [
            {
                test: /\.(js|mjs|jsx)$/,//js文件处理
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['env', 'react','es2015','stage-0'],
                        plugins: ["transform-decorators-legacy"]
                    }
                }
            },
            {
                test: /\.css/,  //antd,animate css文件处理
                include: /node_modules/,
                use: comPlugInCss.extract({
                    fallback: "style-loader",
                    use: "css-loader"
                })
            },
            {
                test: /\.less$/,  //less文件处理
                use: styleCss.extract({
                    fallback: "style-loader",
                    use: ['css-loader','less-loader']
                })
            },
            {
                test: /\.(png|jpg|gif|eot|ttf|woff|woff2|otf)$/,  //图片及字体图标的配置
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 10000,
                            name: 'assert/images/[name].[ext]',
                        },
                    }
                ]
            }
        ]
    },
    resolve: {
        extensions: ['.js', '.jsx', '.less', '.scss', '.css'],
        modules: [
            path.resolve(__dirname, 'node_modules'),
            // path.join(__dirname, './src')
        ],
        // alias是配置全局的路径入口名称，只要涉及到下面配置的文件路径，可以直接用定义的单个字母表示整个路径
        alias: {
            assert: path.join(__dirname, "/src/assert"),
            containers: path.join(__dirname, "/src/containers"),
            component: path.join(__dirname, "/src/component"),
            utils: path.join(__dirname, "/src/utils")
        }
    },
    plugins: [
        new HtmlWebpackPlugin({
            filename: path.resolve(dir, "index.html"),
            template: 'public/index.html',
            inject: true,
            minify: {
                removeComments: true,
                collapseWhitespace: true,
                removeAttributeQuotes: true
            },
            chunksSortMode: "dependency"
        }),
        comPlugInCss,
        styleCss,
        // new OpenBrowserPlugin({ url: 'http://localhost:5211/home' }), //启动默认打开浏览器

        new webpack.DllReferencePlugin({
            context:__dirname,
            manifest: isPro ? require('./dist/dll/manifest.json') : require('./public/dll/manifest.json'),
            name: 'dll',
            inject: true,
        }),
        new webpack.optimize.CommonsChunkPlugin({
            name: "vendor",
            minChunks: function(module) {
                // 该配置假定你引入的 vendor 存在于 node_modules 目录中
                return (
                    module.context && module.context.indexOf("node_modules") !== -1
                );
            }
        }),
        // 删除文件 保留新文件
        /*new CleanWebpackPlugin({
            root: path.resolve(__dirname, 'dist'),
            dry: false // 启用删除文件
        }),*/
    ],
    devServer: {
        port:'5211',
        /*historyApiFallback: {
            index: 'public/index.html'
        },*/
        historyApiFallback:true,
        stats: {
            modules: false,
            chunks: false
        },
        // publicPath: "/",
        // host: '0.0.0.0',
        proxy: {
            '/api': {
                target: 'https://mall-api.qingliu.tk',
                // target: 'https://v1.itooi.cn',
                pathRewrite: {'^/api' : ''},
                changeOrigin: true,     // target是域名的话，需要这个参数，
                secure: false,          // 设置支持https协议的代理
            },
        }
    }
};