function App() {
  const [count, setCount] = React.useState(0);
  function updateCount() {
    setCount(count + 1);
  }
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", null, count), /*#__PURE__*/React.createElement("button", {
    onClick: updateCount
  }, "Count"));
}
document.addEventListener("DOMContentLoaded", () => ReactDOM.render( /*#__PURE__*/React.createElement(App, null), document.querySelector("#app")));