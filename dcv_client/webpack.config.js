/* eslint-disable @typescript-eslint/no-require-imports */
/* eslint-disable no-undef */

const path = require('path');

const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

// noinspection JSUnusedGlobalSymbols
const makeConfig = (mode) => ({
  mode: 'development',
  entry: './src/ts/index.tsx',
  output: {
    path: path.join(__dirname, 'dist'),
    publicPath: '/',
    // See https://github.com/webpack/webpack/issues/10796#issuecomment-717966170
    // This seems to mitigate some memory leak in webpack when constantly rebuilding with new chunk hashes, which
    // happened occasionally to me with webpack-dev-server
    //  - David L, 2025-03-21
    filename: mode === 'production' ? 'js/[name][chunkhash].js' : 'js/[name].js',
    clean: true,
  },
  ...(mode === 'development' ? { devtool: 'inline-source-map' } : {}),
  module: {
    rules: [
      { test: /\.[tj](sx|s)?$/, use: { loader: 'ts-loader' }, exclude: /node_modules/ },
      {
        test: /\.(sass|less|css)$/,
        use: [{ loader: 'style-loader' }, { loader: 'css-loader' }, { loader: 'less-loader' }],
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/i,
        use: [{ loader: 'file-loader' }],
      },
      {
        test: /\.html$/i,
        loader: 'html-loader',
      },
    ],
  },
  watchOptions: {
    aggregateTimeout: 200,
    poll: 1000,
    ignored: /node_modules/,
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'Development',
      inject: false,
    }),
    new CopyWebpackPlugin({
      patterns: [{ from: 'src/static', to: 'static' }],
    }),
  ],
  optimization: {
    runtimeChunk: 'single',
  },
  devtool: 'source-map',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src', 'ts'),
    },
    extensions: ['.tsx', '.ts', '.js'],
  },
});

module.exports = (_env, argv) => makeConfig(argv.mode);
