'use strict';

function App() {

    const [count, setCount] = React.useState(0);

    function updateCount() {
        setCount(count + 1);
    }

    return (
        <div>
            <h1>{count}</h1>
            <button onClick={updateCount}>Count</button>
        </div>
    );
}



document.addEventListener("DOMContentLoaded", () => {
    // @ts-ignore
    ReactDOM.render(<App />, document.querySelector("#app"));
    document.querySelector(".navbar-mobile-button").addEventListener('click', handleMobileMenu);
});

function handleMobileMenu() {
    const element = document.querySelector("#mobile-dropdown");
    if (element.className === "dropdown") {
      element.className += " show";
    } else {
      element.className = "dropdown";
    }
  }