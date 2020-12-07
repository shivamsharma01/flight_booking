import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MainService } from '../service/main.service';

@Component({
  selector: 'app-booking-details',
  templateUrl: './booking-details.component.html',
  styleUrls: ['./booking-details.component.css']
})
export class BookingDetailsComponent implements OnInit {
  detailsForm: FormGroup;
  bookingForm: FormGroup;
  clickedDetails: boolean;
  travelClass: any[] = [{ label: 'Ecomomy', value: 'E' }, { label: 'Business', value: 'B' }, { label: 'First class', value: 'F' }];

  constructor(private _mainService: MainService) { }

  ngOnInit(): void {
    this.initForms();
  }

  initForms() {
    this.clickedDetails = false;
    this.detailsForm = new FormGroup({
      bookingid: new FormControl('')
    });
  }

  viewBooking() {
    if (this._mainService.validateCancel(this.detailsForm.get('bookingid').value)) {
      this._mainService.viewTicket(this.detailsForm.get('bookingid').value).subscribe((data: any) => {
        console.log(data);
        data = JSON.parse(data);
        if (data.error == false) {
          this._mainService.callMessageService("success", 'Info Retrieved for bookingid:'+this.detailsForm.get('bookingid').value);
          this.initDetails(data)
          this.clickedDetails = true
        } else {
          console.log(data.message);
          this._mainService.callMessageService('error', data.message);
        }
      });
    }
  }
  //disable() 
  initDetails(data) {
    this.bookingForm = new FormGroup({
      src: new FormControl(data.src),
      destination: new FormControl(data.dest),
      departureDate: new FormControl(new Date(data.travel_date).toLocaleDateString()),
      flightId: new FormControl(data.flight_id),
      class: new FormControl(this.getClass(data.flight_class)),
      name: new FormControl(data.name),
      bookingstatus: new FormControl(data.booking_status == 'PENDING' ? 'Pending' : 'Confirmed'),
      paymentmethod: new FormControl(data.payment_method == 'PENDING' ? 'Pending' : 'Credit Card'),
      cardnumber: new FormControl((data.card_no == '' || data.card_no == null) ? 'Credit Card Not Added' : data.card_no),
      addon: new FormControl(data.add_on == 'NO' ? 'No add on Facility Availed' : 'Luggage Facility Added'),
      price: new FormControl(this._mainService.dictionary[data.flight_class]),
    });
    this.bookingForm.disable();
  }

  getClass(cur_class) {
    return this.travelClass.find(d => d.value == cur_class)['label'];
  }
}
