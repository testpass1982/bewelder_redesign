const path = require("path");

module.exports = {
  entry: "./dialogs_front/main.js",
  output: {
    filename: "dialog.js",
    path: path.resolve(__dirname, "static/js")
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  }
};
