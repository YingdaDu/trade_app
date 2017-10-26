import React from 'react';
import ReactDOM  from 'react-dom';
import { Button, Col} from 'react-bootstrap';
import './form.css';
export class RegisterForm extends React.Component {
 render()
    {
   return(
     <div className="form">
     <Col>
     <h1>Register</h1>
     <form action="/register" method="post" id="register_form">
     <h3>Name</h3>
       <input
        name="username"
        type="text"
        placeholder="Username"
       />
       <h3>Password</h3>
       <input
        name="password"
        type="password"
        placeholder="Password"
       />
       <h3>Checking deposit</h3>
       <input type="number" name="check" placeholder="checking desposit"/>
       <h3>Trading deposit</h3>
       <input type="number" name="trade" placeholder="trading desposit" />
       <p></p>
       <Button type="submit" bsStyle="success">Submit</Button>
        </form>
      </Col>
    </div>
    )
    }
}
ReactDOM.render(
    <RegisterForm />, document.getElementById('register'));
