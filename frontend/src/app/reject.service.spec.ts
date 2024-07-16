import { TestBed } from '@angular/core/testing';

import { RejectService } from './reject.service';

describe('RejectService', () => {
  let service: RejectService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RejectService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
