import React from 'react';
import ReactDOM  from 'react-dom';
import { Button, Col} from 'react-bootstrap';
import './form.css';
export class LoginForm extends React.Component {
 render()
    {
   return(
     <div className="form">
     <Col>
     <form action="/" method="post" id="login_form">
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
       <p></p>
       <Button type="submit" bsStyle="success">Submit</Button>
        </form>

         <form action="/register" method="get">
          <Button type="submit" bsStyle="success">register</Button>
         </form>

        </Col>
      </div>

    )
    }
}
ReactDOM.render(
    <LoginForm />, document.getElementById('login'));
