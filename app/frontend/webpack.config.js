var webpack = require('webpack');
var path = require('path');
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var AssetsPlugin = require('assets-webpack-plugin');


module.exports = {
    entry: {
        main: "./js/main.js",
        login: "./js/login.js",
        register: "./js/register.js"  
    },
    output: {
        path: path.resolve(__dirname, 'static'),
        publicPath: "/static/",
        filename: 'scripts/[name]-bundle-[hash].js'
    },
    resolve: {
        extensions: [
            '.jsx', '.js', '.json'
        ],
        modules: [
            'node_modules',
            path.resolve(__dirname, './node_modules')
        ]
    },
    module: {
        loaders: [
                {
                  test: /\.css$/,
                  loader: 'style-loader'
                }, {
                  test: /\.css$/,
                  loader: 'css-loader',
                  query: {
                    modules: true,
                    localIdentName: '[local]'
                  }
                }, {
                test: /(\.js|\.jsx)$/,
                exclude: /(node_modules)/,
                loader: 'babel-loader',
                query: {
                    presets: ['es2015', 'stage-0', 'react']
                }
            }
        ]
    }
    ,
    plugins: [
        new ExtractTextPlugin('styles/main-bundle-[hash].css'),
        new AssetsPlugin()
    ]
};
