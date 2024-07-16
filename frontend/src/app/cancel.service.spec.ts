import { TestBed } from '@angular/core/testing';

import { CancelService } from './cancel.service';

describe('CancelService', () => {
  let service: CancelService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CancelService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
