import { Component, OnInit } from '@angular/core';
import { CancelServiceService } from './cancel-service.service';

@Component({
  selector: 'app-booking-history',
  templateUrl: './booking-history.component.html',
  styleUrls: ['./booking-history.component.css']
})
export class BookingHistoryComponent implements OnInit {

  bookings: any[] = [];

  selectedBookings: any[] = [];

  constructor(private _cancelService: CancelServiceService) { }

  ngOnInit() {

      this.bookings = [
          {booking_id: "Amy Elsner", src_location: 'amyelsner.png', dest_location : 'hdkj', class : 'jdfhjk', travel_date : 'gghg'},
          {booking_id: "Amy Elsner", src_location: 'amyelsner.png', dest_location : 'hdkj', class : 'jdfhjk', travel_date : 'gghg'},
          {booking_id: "Amy Elsner", src_location: 'amyelsner.png', dest_location : 'hdkj', class : 'jdfhjk', travel_date : 'gghg'},
          {booking_id: "Amy Elsner", src_location: 'amyelsner.png', dest_location : 'hdkj', class : 'jdfhjk', travel_date : 'gghg'},
          {booking_id: "Amy Elsner", src_location: 'amyelsner.png', dest_location : 'hdkj', class : 'jdfhjk', travel_date : 'gghg'}
      ];
  }

  selectedBooking(booking:any) {
    console.log('booking',booking)
    this.selectedBookings.push(booking.booking_id)
  }
  cancelBooings() {
    if(this.selectedBookings.length > 0) {
      let cancelObj = new CancelObject();
      cancelObj.data = this.selectedBookings;
      console.log('canceling tickets: ', cancelObj.data)
      this._cancelService.cancelTicket(cancelObj).subscribe(data => {
        console.log('cancelled')
      }
        )
    }
  }
}
 export class CancelObject {
    type: "cancel"
    data: any[] = []
 }
