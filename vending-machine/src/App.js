
import './App.css';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/home';
import Purchase from './pages/purchase';
import Management from './pages/management'
import './css/navbar.css'

function App() {
  return (
   
      <BrowserRouter>
      <div className = "App">
        <ul className = 'navbar'>
          <li > <Link to = '/' className = 'link'> Home </Link></li>
          <li> <Link to = '/purchase' className = 'link'> Purchase Tool </Link></li>
          <li> <Link to = '/management' className = 'link'> Management Tool </Link> </li>
        </ul>
        

        <Routes>
          <Route exact path = '/' element = {<Home />} />
          <Route exact path = '/purchase' element = {<Purchase />} />
          <Route exact path = '/management' element = {<Management />} />
        </Routes>
       </div>
      </BrowserRouter>
      
    
  );
}

export default App;
