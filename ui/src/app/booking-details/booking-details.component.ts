import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { BookingService } from '../booking/booking.service';

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

  constructor(private _bookingService: BookingService) { }

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
    if (this._bookingService.validateCancel(this.detailsForm.get('bookingid').value)) {
      this._bookingService.viewTicket(this.detailsForm.get('bookingid').value).subscribe((data: any) => {
        console.log(data);
        data = JSON.parse(data);
        if (data.error == false) {
          this._bookingService.callMessageService("success", data.message);
          this.initDetails(data.data)
          this.clickedDetails = true
        } else {
          console.log(data.message);
          this._bookingService.callMessageService('error', data.message);
        }
      });
    }
  }
  //disable() 
  initDetails(data) {
    this.bookingForm = new FormGroup({
      src: new FormControl(data[2]),
      destination: new FormControl(data[3]),
      departureDate: new FormControl(new Date(data[8]).toLocaleDateString()),
      flightId: new FormControl(data[9]),
      class: new FormControl(this.getClass(data[4])),
      name: new FormControl(data[1]),
      bookingstatus: new FormControl(data[5] == 'PENDING' ? 'Pending' : 'Confirmed'),
      paymentmethod: new FormControl(data[6] == 'PENDING' ? 'Pending' : 'Credit Card'),
      cardnumber: new FormControl((data[7] == '' || data[7] == null) ? 'Credit Card Not Added' : data[7]),
      addon: new FormControl(data[10] == 'NO' ? 'No add on Facility Availed' : 'Luggage Facility Added'),
      price: new FormControl(this._bookingService.dictionary[data[4]]),
    });
    this.bookingForm.disable();
  }

  getClass(cur_class) {
    return this.travelClass.find(d => d.value == cur_class)['label'];
  }
}
