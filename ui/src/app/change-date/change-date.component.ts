import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MainService } from '../service/main.service';

@Component({
  selector: 'app-change-date',
  templateUrl: './change-date.component.html',
  styleUrls: ['./change-date.component.css']
})
export class ChangeDateComponent implements OnInit {
  changeForm: FormGroup;
  constructor(private _mainService: MainService) { }

  ngOnInit(): void {
    this.initForms();
  }

  initForms() {
    this.changeForm = new FormGroup({
      bookingid: new FormControl(''),
      departureDate: new FormControl(''),
    });
  }
  
  changeDate() {
    if (this._mainService.validateDateChange(this.changeForm.value)) {
      this._mainService.changeDate(this.changeForm.value).subscribe((data: any) => {
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
