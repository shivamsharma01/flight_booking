import { BrowserModule } from '@angular/platform-browser';
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { MainService } from './service/main.service';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BookingComponent } from './booking/booking.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TabViewModule } from 'primeng/tabview';
import { InputTextModule } from 'primeng/inputtext';
import { CalendarModule } from 'primeng/calendar';
import { CheckboxModule } from 'primeng/checkbox';
import { TableModule } from 'primeng/table';
import { DropdownModule } from 'primeng/dropdown';
import { BookingHistoryComponent } from './booking-history/booking-history.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    BookingComponent,
    BookingHistoryComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    InputTextModule,
    TabViewModule,
    CalendarModule,
    DropdownModule,
    FormsModule,
    TableModule,
    CheckboxModule
  ],
  providers: [MainService],
  bootstrap: [AppComponent]
})
export class AppModule { }
