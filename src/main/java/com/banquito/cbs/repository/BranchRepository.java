package com.banquito.cbs.repository;

import com.banquito.cbs.model.Branch;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface BranchRepository extends MongoRepository<Branch, Integer> {
}
