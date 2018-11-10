import {Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
import {SResult} from './sresult/SResult';
import {environment} from '../environments/environment';
import {HttpClient} from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private http: HttpClient) {
  }

  MOCK_SRESULTS: SResult[] = [
    {title: 'title', text: 'text one', score: 54, tags: ['a', 'b']},
    {title: 'Cats', text: 'Cats are nice', score: 44, tags: ['a']},
    {title: 'Dogs', text: 'I don\'t like dogs', score: 38, tags: ['a', 'b']},
    {title: 'Rain', text: 'Cats and dogs', score: 20, tags: ['b']}
  ];

  getData(query: string): Observable<SResult[]> {
    if (environment.mock_api) {
      return of(this.MOCK_SRESULTS);
    }
    return this.queryData(query);
  }

  queryData(query: string): Observable<SResult[]> {

    const url = environment.base_url + environment.search_request_template;

    url.replace('{%%}', query);
    return this.http.get<SResult[]>(url);
  }
}
