import React, {PropTypes} from 'react';
import './main.css';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import { Button, Row, Col, Grid, Form, FormControl, FormGroup, ControlLabel} from 'react-bootstrap';




class TRow extends React.Component {
  constructor(props) {
      super(props);
  }

  render(){
     var from = this.props.data.from;
     var to = this.props.data.to;
     if (from == this.props.name) from = (<em style={{color:'#ed5249'}}>You</em>);
     if (to == this.props.name) to = (<em style={{color:'#ed5249'}}>You</em>)
     return (
       <tr>
          <th>{from}</th>
          <th>{to}</th>
          <th>{this.props.data.trade_amount}</th>
          <th>{this.props.data.time}</th>
          <th>
          <form><Button bsStyle="success" bsSize="xsmall" >Approved</Button></form>
          </th>
      </tr>
    )


  }
}

class NTRow extends React.Component {
  constructor(props) {
      super(props);
  }

  render(){
    var from = this.props.data.from;
    var to = this.props.data.to;
    if (from == this.props.name) from = (<em style={{color:'#ed5249'}}>You</em>);
    if (to == this.props.name) to = (<em style={{color:'#ed5249'}}>You</em>)
     return (
       <tr>
          <th>{from}</th>
          <th>{to}</th>
          <th>{this.props.data.trade_amount}</th>
          <th>{this.props.data.time}</th>
          <th>
           <Button bsStyle="danger" bsSize="xsmall">Declined</Button>
           <div><em style={{color:'#ed5249'}}>${this.props.data.deposit}</em> should be added to approve the transaction</div>
          </th>
      </tr>
    )


  }
}

class Trans extends React.Component {
  constructor(props) {
      super(props);
  }


  render(){
    const trans = this.props.trans;
    var rows = [];
    for (var i=trans.length-1; i >= 0; i--){
        var row;
        var data = trans[i];
        if(data.approved) {
          row=(<TRow data={data} name={this.props.name}/>)
          rows.push(row);
        } else {
          if (data.from == this.props.name) {
             row=(<NTRow data={data} name={this.props.name}/>)
             rows.push(row);
          }
        }
    }

    return (
      <Col xs={4} sm={4} md={4}>
        <h1>Transactions</h1>
        <table>
        <thead>
          <tr>
            <th>From</th>
            <th>to</th>
            <th>Amount</th>
            <th>Time</th>
          </tr>
          </thead>
           <tbody>
          {rows}
          </tbody>
        </table>
      </Col>
    );
}
}

class Person extends React.Component {
  constructor(props) {
      super(props);
  }
  // checkform() {
  //   console.log("check")
  //   return false;
  // }
  render() {
      return (
  	     <Col xs={6} sm={6} md={6}>
           <div className="pinfo">
           <h1>Hello {this.props.name} !</h1>
           <h3>Checking Account:<em> ${this.props.check_amount}</em></h3>
           <h3>Trading Account: <em>${this.props.trade_amount}</em></h3>
           </div>
           <div className="trans">
            <form action="/trans" method="post">
            <FormGroup controlId="userName" id="trans-form">
               <h1>Transfer To</h1>
               <FormControl componentClass="select" placeholder="select" name="userid">
                {this.props.list.map(function(listValue){
                  return <option value={listValue[0]} key={listValue[0]}>{listValue[1]}</option>;
                })}
               </FormControl>
               <input
                name="amount"
                type="text"
                label="Text"
                placeholder="Amount"
               />
              </FormGroup>
             <Button type="submit" bsSize="large" bsStyle="success">
                 Transfer
             </Button>
           </form>
           </div>
        </Col>
	    );
    }
}


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: -1,
            name: "",
            trans: [],
            check_amount: 0,
            trading_amount: 0,
            userlist: []
        }
    }

    loaddata() {
    	var host = window.location.host;
    	var url = "http://"+host+'/api';
    	$.ajax({
            url: url,
            datatype: 'json',
            success: function (Response) {
                var data = JSON.parse(Response);
                console.log(data);
                this.setState({
                    id: data.id,
                    userlist: data.namelist,
                    name: data.name,
                    check_amount: data.check_amount,
                    trade_amount: data.trade_amount,
                    trans: data.trans
                });
            }.bind(this),
            error: function () {
                console.log("error")
            }
        })
    }

    componentDidMount() {
      this.loaddata();
    }


    render() {
        return (

           <Grid>
                <Row>
    				      <Person name={this.state.name} check_amount={this.state.check_amount}
                  trade_amount={this.state.trade_amount} list={this.state.userlist}
                  cur_id={this.state.id}/>
                  <Trans trans={this.state.trans} name={this.state.name}/>
                </Row>
			     </Grid>

        );
    }
}


export default App;
