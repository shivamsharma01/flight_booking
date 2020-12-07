import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MainService } from '../service/main.service';

@Component({
  selector: 'app-add-on',
  templateUrl: './add-on.component.html',
  styleUrls: ['./add-on.component.css']
})
export class AddOnComponent implements OnInit {
  addOnForm: FormGroup;
  constructor(private _mainService: MainService) { }

  ngOnInit(): void {
    this.initForms();
  }

  initForms() {
    this.addOnForm = new FormGroup({
      bookingid: new FormControl(''),
      ccNumber: new FormControl(''),
    });
  }

  makePayment() {
    if (this._mainService.validateCreditCard(this.addOnForm.get('bookingid').value, this.addOnForm.value)) {
      this._mainService.makeAddOn(this.addOnForm.value).subscribe((data: any) => {
        console.log(data);
        data = JSON.parse(data);
        if (data.error == false) {
          this._mainService.callMessageService("success", data.success_msg);
        } else {
          console.log(data.message);
          this._mainService.callMessageService('error', data.message);
        }
        this.initForms();
      });
    }
  }

}

