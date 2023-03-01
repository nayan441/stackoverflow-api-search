import { Component, OnInit, Input } from '@angular/core';
import { ApiService } from '../api-services.service';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']

})
export class SearchResultsComponent implements OnInit  {
  query = '';
  results: any;
  count = 1;
  is_previous:boolean= false;

  constructor(private apiService: ApiService) {}
  ngOnInit() {
    if (this.count > 1){
      this.is_previous = true
    }
    else{
      this.is_previous = false
    }
    console.log("Next page", this.count, "Previous page", this.is_previous);
    
    
  }
  
  onSearch() {

    this.apiService.search(this.query, this.count, ).subscribe(results => {
      this.results = results;
      console.log(results);


      this.results.reset();
    });
  }
  
  onPageChange() {
    this.count+=1
    if (this.count > 1){
      this.is_previous = true
    }
    else{
      this.is_previous = false
    }
    this.apiService.search(this.query, this.count,).subscribe(results => {
      this.results = results;
      console.log("Next page------------", this.count, "Previous page----", this.is_previous);
    });
  }
  onPageChangePrevious() {
    if (this.count > 1){
    this.count-=1
  }
    if (this.count === 1){
      this.is_previous = false
  }

    this.apiService.search(this.query, this.count,).subscribe(results => {
      this.results = results;
      console.log("Next  page----------------------", this.count, "Previous page----------", this.is_previous);
    });
  }
}