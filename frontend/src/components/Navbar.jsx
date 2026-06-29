import { Link } from "react-router-dom";
import "../styles/navbar.css";

function Navbar() {
  return (
    <nav className="navbar">

      <div className="container nav-content">

        <div className="logo">
          🚧 SmartRoad AI
        </div>

        <div className="nav-links">

          <Link to="/">Home</Link>

          <Link to="/history">History</Link>

          <Link to="/about">About</Link>

        </div>

      </div>

    </nav>
  );
}

export default Navbar;