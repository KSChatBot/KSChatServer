var HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');

module.exports = {
    mode: 'development',
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