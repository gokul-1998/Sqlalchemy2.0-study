```
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (1, 'Europe', NULL);

INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (2, 'Asia',   NULL);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (3, 'Africa',   NULL);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (4, 'France',  1);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (5, 'India',   2);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (6, 'China', 2);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (7, 'Zimbabwe', 3);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (8, 'Hong Kong', 6);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (9, 'Beijing', 6);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (10, 'Shanghai',6);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (11, 'Chandigarh', 5);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (12, 'Mumbai', 5);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (13, 'Delhi', 5);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (14, 'Haryana', 5);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (15, 'Gurgaon', 14);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (16, 'Panchkula', 14);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (17, 'Paris', 4);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (18, 'Marseille', 4);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (19, 'Harare', 7);
INSERT INTO tbHierarchy(Id, Name, ParentId)
    VALUES (20, 'Bulawayo', 7); 
```