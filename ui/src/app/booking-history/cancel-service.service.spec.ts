import { TestBed } from '@angular/core/testing';

import { CancelServiceService } from './cancel-service.service';

describe('CancelServiceService', () => {
  let service: CancelServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CancelServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
