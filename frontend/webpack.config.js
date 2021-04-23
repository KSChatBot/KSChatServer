var HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');
const mode = process.env.NODE_ENV || "development" // 기본값을 development로 설정

console.log("환경:",process.env.NODE_ENV)

module.exports = {
    mode,
    entry: './src/index.jsx',                            // 리액트 파일이 시작하는 곳
    output: {                                           // bundled compiled 파일
        path: path.join(__dirname, '/build'),            //__dirname : 현재 디렉토리, dist 폴더에 모든 컴파일된 하나의 번들파일을 넣을 예정
        filename: 'index_bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                loader: 'babel-loader', exclude: /node_modules/
            },
            {
                test: /\.less$/,
                use: [
                    { loader: 'style-loader' },
                    { loader: 'css-loader' },
                    { loader: 'less-loader' }
                ]
            }
        ]
    },
    resolve: {
        mainFiles: ['index', 'Index'],
        extensions: ['.js', '.jsx'],
        alias: {
            '@': path.resolve(__dirname, 'src/'),
        }
    },
    plugins: [new HtmlWebpackPlugin({
        template: './public/index.html'
    })],
    devServer: {
        disableHostCheck: true,
        historyApiFallback: true,
        host: '0.0.0.0',
        contentBase: path.join(__dirname, 'public')
    },
    externals: {
        // global app config object
        config: JSON.stringify({
            // apiUrl: 'http://koreascoring.iptime.org:8081'
            apiUrl: 'http://localhost:8081'
        })
    }
}